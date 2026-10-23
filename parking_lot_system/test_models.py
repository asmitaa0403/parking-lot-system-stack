"""
Unit test suite for the Parking Stack models and algorithms.
"""
from datetime import datetime, timedelta
from models import Vehicle, ParkingStack, ParkingManager

def test_stack_basic_operations():
    stack = ParkingStack("lane_1", "Lane 1", capacity=3)
    assert stack.is_empty()
    assert not stack.is_full()
    assert stack.size() == 0

    v1 = Vehicle("CAR-1", "Alice")
    v2 = Vehicle("CAR-2", "Bob")
    v3 = Vehicle("CAR-3", "Charlie")
    v4 = Vehicle("CAR-4", "Dave")

    assert stack.push(v1) is True
    assert stack.push(v2) is True
    assert stack.push(v3) is True
    # Capacity is 3, 4th push should fail
    assert stack.push(v4) is False
    assert stack.is_full()
    assert stack.size() == 3

    # Top vehicle should be CAR-3
    assert stack.peek().plate == "CAR-3"

    # Positions: CAR-3 is depth 0, CAR-2 is depth 1, CAR-1 is depth 2
    assert stack.find_position("CAR-3") == 0
    assert stack.find_position("CAR-2") == 1
    assert stack.find_position("CAR-1") == 2
    assert stack.find_position("NON-EXISTENT") == -1

    # Pop should return CAR-3
    popped = stack.pop()
    assert popped.plate == "CAR-3"
    assert stack.size() == 2
    print("test_stack_basic_operations passed!")

def test_parking_manager_auxiliary_retrieval():
    mgr = ParkingManager(num_lanes=1, lane_capacity=5, hourly_rate=10.0)
    
    # Park 3 cars: CAR-A (bottom), CAR-B (middle), CAR-C (top)
    vA = Vehicle("CAR-A", "Alice", entry_time=datetime.now() - timedelta(hours=2))
    vB = Vehicle("CAR-B", "Bob", entry_time=datetime.now() - timedelta(hours=1))
    vC = Vehicle("CAR-C", "Charlie", entry_time=datetime.now() - timedelta(minutes=30))

    mgr.park(vA, "lane_1")
    mgr.park(vB, "lane_1")
    mgr.park(vC, "lane_1")

    # Lane stack order from bottom to top: [CAR-A, CAR-B, CAR-C]
    # Now retrieve CAR-A (depth 2: blocked by CAR-C and CAR-B)
    departed, receipt, logs = mgr.unpark_by_plate("CAR-A")

    assert departed.plate == "CAR-A"
    assert receipt["total_fee"] > 0
    # Moves count: pop CAR-C (1) -> pop CAR-B (2) -> pop CAR-A (3) -> push CAR-B (4) -> push CAR-C (5)
    assert receipt["moves_count"] == 5

    # Remaining in stack: [CAR-B, CAR-C] in original order!
    lane = mgr.lanes["lane_1"]
    assert lane.size() == 2
    remaining_plates = [v.plate for v in lane.get_items()]
    assert remaining_plates == ["CAR-B", "CAR-C"]
    assert lane.peek().plate == "CAR-C"
    print("test_parking_manager_auxiliary_retrieval passed!")

if __name__ == "__main__":
    test_stack_basic_operations()
    test_parking_manager_auxiliary_retrieval()
    print("All unit tests passed successfully!")
