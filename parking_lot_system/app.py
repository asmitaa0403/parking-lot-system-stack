import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

from models import ParkingManager, Vehicle
import styles

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmartPark - LIFO Stack Parking System",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS styling
st.markdown(styles.CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "parking_manager" not in st.session_state:
    st.session_state.parking_manager = ParkingManager(num_lanes=3, lane_capacity=5, hourly_rate=50.0)

if "last_operation_logs" not in st.session_state:
    st.session_state.last_operation_logs = []

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

mgr: ParkingManager = st.session_state.parking_manager

# ---------------------------------------------------------
# Preset Demo Data Loader
# ---------------------------------------------------------
def load_demo_cars():
    """Populates lanes with realistic test cars for quick testing."""
    sample_cars = [
        ("ABC-101", "Alice Smith", "Sedan", "#3b82f6", 110),
        ("XYZ-992", "Bob Johnson", "SUV", "#ef4444", 95),
        ("TES-404", "Charlie Brown", "EV", "#10b981", 80),
        ("MOTO-77", "Diana Prince", "Motorcycle", "#f59e0b", 60),
        ("VAN-888", "Ethan Hunt", "Van", "#8b5cf6", 45),
        ("TRK-303", "Fiona Gallagher", "Truck", "#ec4899", 30),
        ("NYC-555", "George Clark", "Sedan", "#06b6d4", 15),
    ]

    for plate, owner, vtype, color, minutes_ago in sample_cars:
        if mgr.find_vehicle(plate) is None:
            v = Vehicle(
                plate=plate,
                owner=owner,
                vehicle_type=vtype,
                color=color,
                entry_time=datetime.now() - timedelta(minutes=minutes_ago),
                rate_per_hour=mgr.hourly_rate
            )
            mgr.park(v)

def reset_all():
    """Clears all lanes and state."""
    st.session_state.parking_manager = ParkingManager(
        num_lanes=len(mgr.lanes),
        lane_capacity=mgr.lane_capacity,
        hourly_rate=mgr.hourly_rate
    )
    st.session_state.last_operation_logs = []
    st.session_state.last_receipt = None

# ---------------------------------------------------------
# Sidebar Controls & System Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    
    st.markdown("#### 📐 Stack Parameters")
    num_lanes_choice = st.slider("Number of Lanes (Stacks)", min_value=1, max_value=5, value=len(mgr.lanes))
    capacity_choice = st.slider("Stack Capacity per Lane", min_value=3, max_value=8, value=mgr.lane_capacity)
    hourly_rate_choice = st.number_input("Hourly Parking Rate (₹)", min_value=5.0, max_value=500.0, value=mgr.hourly_rate, step=5.0)
    
    # If parameters changed, offer resize/reset
    if (num_lanes_choice != len(mgr.lanes) or 
        capacity_choice != mgr.lane_capacity or 
        hourly_rate_choice != mgr.hourly_rate):
        if st.button("Apply New Lot Configuration (Resets Data)"):
            st.session_state.parking_manager = ParkingManager(
                num_lanes=num_lanes_choice,
                lane_capacity=capacity_choice,
                hourly_rate=hourly_rate_choice
            )
            st.session_state.last_operation_logs = []
            st.session_state.last_receipt = None
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🧪 Test Actions")
    col_demo, col_reset = st.columns(2)
    with col_demo:
        if st.button("📥 Load Demo", use_container_width=True):
            load_demo_cars()
            st.rerun()
    with col_reset:
        if st.button("🗑️ Reset Lot", use_container_width=True):
            reset_all()
            st.rerun()

    st.markdown("---")
    st.markdown("""
    #### 📚 Stack (LIFO) Concept:
    - **Dead-end Driveway Model**: Each parking lane acts as a single-ended stack.
    - **Push**: New incoming cars are placed at the top (exit gate end).
    - **Direct Pop**: The most recently parked car exits in **O(1)**.
    - **Arbitrary Retrieval**: To remove a buried car, blocking cars are popped into a **Buffer Stack** and pushed back in exact order!
    """)

# ---------------------------------------------------------
# Main App Header & Metrics
# ---------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <h1>🅿️ SmartPark — Stack-Based Parking System</h1>
    <p class="hero-subtitle">Visualizing Last-In-First-Out (LIFO) Data Structure in Real-World Dead-End Parking Lanes</p>
</div>
""", unsafe_allow_html=True)

metrics = mgr.get_summary_metrics()

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{metrics['occupied']} / {metrics['total_capacity']}</div>
        <div class="metric-label">Occupancy</div>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{metrics['available']}</div>
        <div class="metric-label">Available Slots</div>
    </div>
    """, unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">₹{metrics['total_revenue']:.2f}</div>
        <div class="metric-label">Total Revenue</div>
    </div>
    """, unsafe_allow_html=True)
with col_m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{metrics['total_operations']}</div>
        <div class="metric-label">Stack Ops (Pushes/Pops)</div>
    </div>
    """, unsafe_allow_html=True)
with col_m5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{metrics['total_departed']}</div>
        <div class="metric-label">Departed Cars</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# Visual Parking Lot (Stack Visualization)
# ---------------------------------------------------------
st.markdown("### 🚘 Real-Time Stack Lanes Visualizer")

lane_cols = st.columns(len(mgr.lanes))

for i, (lane_id, lane) in enumerate(mgr.lanes.items()):
    with lane_cols[i]:
        st.markdown(f"""
        <div class="lane-container">
            <div class="lane-title">
                <span>{lane.name}</span>
                <span style="font-size:0.8rem; font-weight:normal; color:#94a3b8;">
                    {lane.size()}/{lane.capacity} Cars
                </span>
            </div>
            <div class="stack-gate-indicator">
                ⬇️ EXIT & ENTRY GATE (TOP OF STACK) ⬆️
            </div>
        """, unsafe_allow_html=True)

        items = lane.get_items()
        
        # Render stack from TOP (exit gate) to BOTTOM (dead end)
        # In Python list: index -1 is top, index 0 is bottom
        if items:
            for depth, vehicle in enumerate(reversed(items)):
                is_top = (depth == 0)
                st.markdown(styles.render_vehicle_card(vehicle, depth, is_top=is_top), unsafe_allow_html=True)
        else:
            st.info("Lane is currently empty.")

        # Show empty slots remaining
        empty_count = lane.capacity - lane.size()
        for empty_slot_idx in range(empty_count):
            slot_num = lane.size() + empty_slot_idx + 1
            st.markdown(styles.render_empty_slot(slot_num), unsafe_allow_html=True)

        st.markdown("""
            <div class="stack-bottom-indicator">
                🛑 DEAD-END (STACK BASE / INDEX 0)
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Action Tabs: Operations & Algorithms
# ---------------------------------------------------------
st.markdown("---")
tab_park, tab_unpark_target, tab_quick_pop, tab_search, tab_history = st.tabs([
    "📥 1. Park Vehicle (PUSH)",
    "🔄 2. Retrieve Specific Vehicle (Stack Algorithm)",
    "⚡ 3. Fast LIFO Exit (Direct POP)",
    "🔍 4. Vehicle Locator",
    "📊 5. Audit Logs & Receipts"
])

# ---------------------------------------------------------
# Tab 1: Park Vehicle (PUSH)
# ---------------------------------------------------------
with tab_park:
    st.subheader("Park a Vehicle (Push onto Stack)")
    with st.form("park_form", clear_on_submit=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            plate_input = st.text_input("License Plate", placeholder="e.g. ABC-7890").upper()
            owner_input = st.text_input("Owner Name", placeholder="e.g. John Doe")
        with col_f2:
            vtype_input = st.selectbox("Vehicle Type", ["Sedan", "SUV", "EV", "Truck", "Motorcycle", "Van"])
            color_choice = st.color_picker("Vehicle Color Identifier", "#3b82f6")
        with col_f3:
            lane_options = ["Auto-Assign (Optimal)"] + [f"{l.name} ({l.size()}/{l.capacity})" for l in mgr.lanes.values()]
            selected_lane_option = st.selectbox("Assign Lane", lane_options)

        submitted = st.form_submit_button("🚀 Park Vehicle (PUSH to Stack)", use_container_width=True)
        if submitted:
            if not plate_input.strip() or not owner_input.strip():
                st.error("Please provide both License Plate and Owner Name.")
            else:
                target_lane_id = None
                if selected_lane_option != "Auto-Assign (Optimal)":
                    # extract lane_id
                    for lid, l in mgr.lanes.items():
                        if l.name in selected_lane_option:
                            target_lane_id = lid
                            break

                new_vehicle = Vehicle(
                    plate=plate_input,
                    owner=owner_input,
                    vehicle_type=vtype_input,
                    color=color_choice,
                    rate_per_hour=mgr.hourly_rate
                )

                success, msg = mgr.park(new_vehicle, target_lane_id)
                if success:
                    st.success(msg)
                    st.session_state.last_operation_logs = [f"[PUSH] {msg}"]
                    st.rerun()
                else:
                    st.error(msg)

# ---------------------------------------------------------
# Tab 2: Retrieve Specific Vehicle (Auxiliary Stack Re-ordering)
# ---------------------------------------------------------
with tab_unpark_target:
    st.subheader("Retrieve Any Parked Vehicle (Multi-Stack Algorithm)")
    st.write(
        "If a vehicle is parked deep in the lane, the system automatically relocates all blocking vehicles "
        "onto a **Temporary Buffer Stack**, pops the target vehicle, and restores the blocking vehicles back to their original spots."
    )

    all_parked = []
    for lid, lane in mgr.lanes.items():
        for vehicle in lane.get_items():
            depth = lane.find_position(vehicle.plate)
            all_parked.append((vehicle.plate, lane.name, depth, vehicle.owner, vehicle.vehicle_type))

    if not all_parked:
        st.info("No vehicles currently parked in the parking lot.")
    else:
        # Build dropdown options
        plate_choices = [
            f"{p[0]} — {p[1]} (Depth: {p[2]} car{'s' if p[2]!=1 else ''} blocking) | Owner: {p[3]}"
            for p in all_parked
        ]
        selected_choice = st.selectbox("Select Target Vehicle to Retrieve:", plate_choices)
        selected_plate = selected_choice.split(" — ")[0].strip()

        # Find depth and details
        found_info = mgr.find_vehicle(selected_plate)
        if found_info:
            lane, depth, target_car = found_info
            
            c_info1, c_info2 = st.columns([2, 1])
            with c_info1:
                if depth == 0:
                    st.success(f"🎯 **{target_car.plate}** is right at the exit! Only **1 POP** operation needed.")
                else:
                    st.warning(
                        f"⚠️ **{target_car.plate}** is blocked by **{depth}** vehicle(s).\n\n"
                        f"Algorithm Plan: **{depth} Pops** to Buffer Stack ➡️ **1 Pop** for Target ➡️ **{depth} Pushes** back to {lane.name}. "
                        f"Total operations: **{2 * depth + 1} stack moves**."
                    )
            with c_info2:
                if st.button("🔄 Execute Auxiliary Stack Retrieval", type="primary", use_container_width=True):
                    departed, receipt, logs = mgr.unpark_by_plate(selected_plate)
                    st.session_state.last_operation_logs = logs
                    st.session_state.last_receipt = receipt
                    st.rerun()

# ---------------------------------------------------------
# Tab 3: Fast LIFO Exit (Direct POP)
# ---------------------------------------------------------
with tab_quick_pop:
    st.subheader("Direct LIFO Departure (Exit Top of Stack)")
    st.write("Perform an instant $O(1)$ stack `pop()` for the vehicle at the top of each lane.")

    cols_direct = st.columns(len(mgr.lanes))
    for i, (lid, lane) in enumerate(mgr.lanes.items()):
        with cols_direct[i]:
            st.markdown(f"**{lane.name}**")
            top_car = lane.peek()
            if top_car:
                st.info(f"Top: **{top_car.plate}** ({top_car.vehicle_type})\n\nOwner: {top_car.owner}")
                if st.button(f"🚪 Direct POP from {lane.name}", key=f"pop_{lid}", use_container_width=True):
                    departed, receipt, logs = mgr.unpark_direct(lid)
                    st.session_state.last_operation_logs = logs
                    st.session_state.last_receipt = receipt
                    st.rerun()
            else:
                st.caption("No vehicle at exit.")

# ---------------------------------------------------------
# Tab 4: Vehicle Locator
# ---------------------------------------------------------
with tab_search:
    st.subheader("Vehicle Stack Locator")
    search_query = st.text_input("Search by License Plate or Owner Name:", placeholder="Type plate or name...").strip().upper()

    if search_query:
        found_results = []
        for lid, lane in mgr.lanes.items():
            for idx, vehicle in enumerate(lane.get_items()):
                if search_query in vehicle.plate or search_query.lower() in vehicle.owner.lower():
                    depth = lane.find_position(vehicle.plate)
                    found_results.append({
                        "Plate": vehicle.plate,
                        "Owner": vehicle.owner,
                        "Type": vehicle.vehicle_type,
                        "Lane": lane.name,
                        "Position (From Base)": f"Slot {idx + 1}",
                        "Depth (From Exit)": depth,
                        "Status": "Ready to Exit" if depth == 0 else f"{depth} car(s) ahead",
                        "Parked At": vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S")
                    })
        if found_results:
            st.dataframe(pd.DataFrame(found_results), use_container_width=True)
        else:
            st.warning(f"No vehicles matching '{search_query}' found.")

# ---------------------------------------------------------
# Tab 5: Analytics & Receipts
# ---------------------------------------------------------
with tab_history:
    st.subheader("Transaction History & Billing")
    if mgr.history:
        df_hist = pd.DataFrame(mgr.history)
        st.dataframe(
            df_hist[[
                "plate", "owner", "vehicle_type", "entry_time", "exit_time",
                "duration_str", "moves_count", "base_fee", "move_fee", "total_fee"
            ]].rename(columns={
                "plate": "Plate",
                "owner": "Owner",
                "vehicle_type": "Type",
                "entry_time": "Entry Time",
                "exit_time": "Exit Time",
                "duration_str": "Duration",
                "moves_count": "Stack Moves",
                "base_fee": "Base Fee (₹)",
                "move_fee": "Handling Fee (₹)",
                "total_fee": "Total Paid (₹)"
            }),
            use_container_width=True
        )

        csv = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Receipts as CSV",
            data=csv,
            file_name=f"parking_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No transaction history yet. Retrieve a parked vehicle to generate checkout receipts.")

# ---------------------------------------------------------
# Real-Time Algorithm Execution Logs & Latest Receipt Box
# ---------------------------------------------------------
if st.session_state.last_operation_logs or st.session_state.last_receipt:
    st.markdown("---")
    col_receipt, col_console = st.columns([1, 1])

    with col_receipt:
        if st.session_state.last_receipt:
            rc = st.session_state.last_receipt
            st.markdown(f"""
            <div class="receipt-card">
                <h4 style="margin-top:0; color:#38bdf8; display:flex; justify-content:space-between;">
                    <span>🧾 Checkout Receipt</span>
                    <span>{rc['plate']}</span>
                </h4>
                <p style="margin: 0.2rem 0; font-size: 0.85rem; color:#cbd5e1;"><strong>Driver:</strong> {rc['owner']} ({rc['vehicle_type']})</p>
                <p style="margin: 0.2rem 0; font-size: 0.85rem; color:#cbd5e1;"><strong>Duration:</strong> {rc['duration_str']}</p>
                <p style="margin: 0.2rem 0; font-size: 0.85rem; color:#cbd5e1;"><strong>Entry:</strong> {rc['entry_time']}</p>
                <p style="margin: 0.2rem 0; font-size: 0.85rem; color:#cbd5e1;"><strong>Exit:</strong> {rc['exit_time']}</p>
                <hr style="border-color:#334155; margin: 0.5rem 0;" />
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#94a3b8;">
                    <span>Base Parking Fee:</span>
                    <span>₹{rc['base_fee']:.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#94a3b8;">
                    <span>Stack Move Fee ({rc['moves_count']} moves):</span>
                    <span>₹{rc['move_fee']:.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:1.1rem; font-weight:700; color:#22c55e; margin-top:0.5rem;">
                    <span>Total Paid:</span>
                    <span>₹{rc['total_fee']:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Execute an unpark action to view departure billing receipt.")

    with col_console:
        if st.session_state.last_operation_logs:
            st.markdown("#### 💻 Stack Operation Execution Log")
            log_entries = "<br>".join(st.session_state.last_operation_logs)
            st.markdown(f"""
            <div class="algo-log-box">
                {log_entries}
            </div>
            """, unsafe_allow_html=True)
