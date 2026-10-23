import time
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any

class Vehicle:
    def __init__(
        self,
        plate: str,
        owner: str,
        vehicle_type: str = "Sedan",
        color: str = "#3b82f6",
        entry_time: Optional[datetime] = None,
        rate_per_hour: float = 50.0
    ):
        self.plate = plate.strip().upper()
        self.owner = owner.strip()
        self.vehicle_type = vehicle_type
        self.color = color
        self.entry_time = entry_time or datetime.now()
        self.rate_per_hour = rate_per_hour

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plate": self.plate,
            "owner": self.owner,
            "vehicle_type": self.vehicle_type,
            "color": self.color,
            "entry_time": self.entry_time.isoformat(),
            "rate_per_hour": self.rate_per_hour,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        return cls(
            plate=data["plate"],
            owner=data["owner"],
            vehicle_type=data.get("vehicle_type", "Sedan"),
            color=data.get("color", "#3b82f6"),
            entry_time=datetime.fromisoformat(data["entry_time"]),
            rate_per_hour=data.get("rate_per_hour", 50.0),
        )


class ParkingStack:
    """
    Implements a classic LIFO (Last-In-First-Out) stack representing a single-lane
    driveway where cars enter and exit from the same open end (the top of the stack).
    """
    def __init__(self, lane_id: str, name: str, capacity: int = 5):
        self.lane_id = lane_id
        self.name = name
        self.capacity = capacity
        self._items: List[Vehicle] = []

    def push(self, vehicle: Vehicle) -> bool:
        """Pushes a vehicle onto the stack if capacity allows."""
        if self.is_full():
            return False
        self._items.append(vehicle)
        return True

    def pop(self) -> Optional[Vehicle]:
        """Pops and returns the vehicle at the top (exit end) of the stack."""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Vehicle]:
        """Looks at the vehicle at the top of the stack without removing it."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def is_full(self) -> bool:
        return len(self._items) >= self.capacity

    def size(self) -> int:
        return len(self._items)

    def get_items(self) -> List[Vehicle]:
        """Returns a copy of the items list (index 0 is bottom, index -1 is top)."""
        return list(self._items)

    def find_position(self, plate: str) -> int:
        """
        Returns 0-based depth from top:
        0 means at the top (ready to exit directly).
        >0 means vehicles are above it.
        -1 if not found.
        """
        for i, v in enumerate(reversed(self._items)):
            if v.plate == plate:
                return i
        return -1


class ParkingManager:
    """
    Orchestrates multiple parking stack lanes, temporary buffer stacks,
    complex arbitrary vehicle retrieval (via auxiliary stacks), and billing.
    """
    def __init__(self, num_lanes: int = 3, lane_capacity: int = 5, hourly_rate: float = 50.0):
        self.lanes: Dict[str, ParkingStack] = {}
        self.lane_capacity = lane_capacity
        self.hourly_rate = hourly_rate
        self.total_revenue = 0.0
        self.total_operations_count = 0
        self.history: List[Dict[str, Any]] = []

        for i in range(1, num_lanes + 1):
            lane_id = f"lane_{i}"
            self.lanes[lane_id] = ParkingStack(lane_id, f"Lane {i}", lane_capacity)

    def park(self, vehicle: Vehicle, lane_id: Optional[str] = None) -> Tuple[bool, str]:
        """
        Parks a vehicle into a specific lane or the first available lane.
        """
        # Check if already parked
        if self.find_vehicle(vehicle.plate) is not None:
            return False, f"Vehicle with plate {vehicle.plate} is already parked in the lot!"

        target_lane: Optional[ParkingStack] = None
        if lane_id and lane_id in self.lanes:
            if not self.lanes[lane_id].is_full():
                target_lane = self.lanes[lane_id]
            else:
                return False, f"{self.lanes[lane_id].name} is completely full (Capacity: {self.lane_capacity})!"
        else:
            # Auto-assign to lane with fewest cars or first non-full lane
            available = [lane for lane in self.lanes.values() if not lane.is_full()]
            if not available:
                return False, "All parking lanes are currently at maximum capacity!"
            # Choose the one with lowest occupancy
            target_lane = min(available, key=lambda l: l.size())

        vehicle.rate_per_hour = self.hourly_rate
        success = target_lane.push(vehicle)
        if success:
            self.total_operations_count += 1
            return True, f"Vehicle {vehicle.plate} successfully pushed onto {target_lane.name} (Position: Slot {target_lane.size()}/{target_lane.capacity})."
        return False, "Failed to park vehicle."

    def find_vehicle(self, plate: str) -> Optional[Tuple[ParkingStack, int, Vehicle]]:
        """
        Locates vehicle across all lanes.
        Returns: (lane, depth_from_top, vehicle) or None
        """
        plate = plate.strip().upper()
        for lane in self.lanes.values():
            depth = lane.find_position(plate)
            if depth != -1:
                # Find vehicle object
                for v in lane.get_items():
                    if v.plate == plate:
                        return lane, depth, v
        return None

    def unpark_direct(self, lane_id: str) -> Tuple[Optional[Vehicle], Dict[str, Any], List[str]]:
        """
        Pops the top vehicle directly from a given lane stack.
        O(1) LIFO pop operation.
        """
        lane = self.lanes.get(lane_id)
        if not lane or lane.is_empty():
            return None, {}, ["Selected lane is already empty."]

        logs = []
        logs.append(f"Direct LIFO Exit triggered on {lane.name}.")
        vehicle = lane.pop()
        self.total_operations_count += 1
        logs.append(f"[POP] Car {vehicle.plate} popped from top of {lane.name}.")

        receipt = self._generate_receipt(vehicle, moves_count=1)
        self.total_revenue += receipt["total_fee"]
        self.history.append(receipt)
        return vehicle, receipt, logs

    def unpark_by_plate(self, plate: str) -> Tuple[Optional[Vehicle], Dict[str, Any], List[str]]:
        """
        Retrieves an arbitrary vehicle from anywhere in the stack using an auxiliary stack.
        Algorithm:
        1. Identify the lane and the depth of target vehicle.
        2. Pop all cars above the target onto an Auxiliary Buffer Stack.
        3. Pop the target car (departure).
        4. Pop cars from Auxiliary Stack and push them back into the Lane Stack in original order.
        """
        found = self.find_vehicle(plate)
        if not found:
            return None, {}, [f"Vehicle with plate {plate} not found in any lane."]

        lane, depth, target_vehicle = found
        logs = []
        moves = 0
        auxiliary_stack: List[Vehicle] = []

        logs.append(f"Initiating Stack Retrieval for {target_vehicle.plate} in {lane.name} (Depth from exit: {depth}).")

        # Step 1: Pop blocking cars into auxiliary stack
        if depth > 0:
            logs.append(f"Cars blocking the exit: {depth}. Relocating them to Temporary Buffer Stack...")
            for step in range(depth):
                blocked_car = lane.pop()
                moves += 1
                self.total_operations_count += 1
                auxiliary_stack.append(blocked_car)
                logs.append(f"  -> [POP from {lane.name}] Car {blocked_car.plate} moved to [Buffer Stack PUSH].")

        # Step 2: Pop target car
        departed_car = lane.pop()
        moves += 1
        self.total_operations_count += 1
        logs.append(f"[TARGET POPPED] Target vehicle {departed_car.plate} exited {lane.name}!")

        # Step 3: Restore cars from auxiliary stack back to lane
        if auxiliary_stack:
            logs.append("Restoring blocking cars from Temporary Buffer Stack back into Lane Stack...")
            while auxiliary_stack:
                restored_car = auxiliary_stack.pop()
                lane.push(restored_car)
                moves += 1
                self.total_operations_count += 1
                logs.append(f"  <- [POP from Buffer Stack] Car {restored_car.plate} restored to [{lane.name} PUSH].")

        logs.append(f"Stack restoration complete. Total stack moves executed: {moves}.")

        # Generate receipt with small move penalty or operational handling fee if depth > 0
        receipt = self._generate_receipt(departed_car, moves_count=moves)
        self.total_revenue += receipt["total_fee"]
        self.history.append(receipt)

        return departed_car, receipt, logs

    def _generate_receipt(self, vehicle: Vehicle, moves_count: int) -> Dict[str, Any]:
        exit_time = datetime.now()
        duration_seconds = max(10, int((exit_time - vehicle.entry_time).total_seconds()))
        # Billing: calculate hours (minimum 1 hour base or fractional for simulation)
        # For demonstration purposes, we support 1 min = 1 hour simulation scaling or pure minutes
        hours = max(0.1, duration_seconds / 3600.0)
        base_fee = round(hours * vehicle.rate_per_hour, 2)
        # Extra handling fee for multi-stack shuffling (₹10.00 per auxiliary move)
        move_fee = round(max(0, moves_count - 1) * 10.0, 2)
        total_fee = round(base_fee + move_fee, 2)

        return {
            "plate": vehicle.plate,
            "owner": vehicle.owner,
            "vehicle_type": vehicle.vehicle_type,
            "entry_time": vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_str": self._format_duration(duration_seconds),
            "duration_seconds": duration_seconds,
            "base_fee": base_fee,
            "move_fee": move_fee,
            "moves_count": moves_count,
            "total_fee": total_fee,
        }

    @staticmethod
    def _format_duration(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs} seconds"

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_capacity = sum(lane.capacity for lane in self.lanes.values())
        occupied = sum(lane.size() for lane in self.lanes.values())
        return {
            "total_capacity": total_capacity,
            "occupied": occupied,
            "available": total_capacity - occupied,
            "total_revenue": round(self.total_revenue, 2),
            "total_operations": self.total_operations_count,
            "total_departed": len(self.history)
        }
