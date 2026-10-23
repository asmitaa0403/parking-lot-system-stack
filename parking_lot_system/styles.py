"""
Custom CSS styles and styling helpers for Parking Lot Management System.
"""

CUSTOM_CSS = """
<style>
/* Main app layout adjustments */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 95%;
}

/* Header Banner */
.hero-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #334155;
    color: #f8fafc;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.hero-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    color: #60a5fa;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0;
}

/* KPI metric cards */
.metric-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #38bdf8;
}
.metric-label {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Parking Stack Lane Container */
.lane-container {
    background: #0f172a;
    border: 2px solid #334155;
    border-radius: 12px;
    padding: 0.75rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}

.lane-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #334155;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stack-gate-indicator {
    background: rgba(37, 99, 235, 0.15);
    border: 1px dashed #3b82f6;
    color: #60a5fa;
    border-radius: 6px;
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    text-align: center;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
}

.stack-bottom-indicator {
    background: #1e293b;
    border-top: 3px solid #64748b;
    color: #94a3b8;
    border-radius: 0 0 6px 6px;
    padding: 0.25rem;
    font-size: 0.7rem;
    text-align: center;
    margin-top: 0.4rem;
}

/* Vehicle Card inside Stack */
.vehicle-card {
    background: #1e293b;
    border-radius: 8px;
    padding: 0.6rem 0.75rem;
    margin-bottom: 0.4rem;
    border-left: 5px solid #3b82f6;
    border-top: 1px solid #334155;
    border-right: 1px solid #334155;
    border-bottom: 1px solid #334155;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: transform 0.15s ease-in-out;
}

.vehicle-card:hover {
    transform: translateY(-2px);
    border-color: #60a5fa;
}

.top-vehicle-card {
    border-left-color: #22c55e !important;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.25);
}

.vehicle-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.25rem;
}

.plate-badge {
    background: #0f172a;
    color: #f1f5f9;
    font-family: 'Consolas', 'Courier New', monospace;
    font-weight: 800;
    font-size: 0.95rem;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    border: 1px solid #475569;
    letter-spacing: 0.06em;
}

.type-tag {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    background: #334155;
    color: #cbd5e1;
}

.vehicle-meta {
    font-size: 0.75rem;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    margin-top: 0.25rem;
}

/* Empty parking slot */
.empty-slot {
    border: 1px dashed #475569;
    border-radius: 8px;
    padding: 0.75rem 0.5rem;
    margin-bottom: 0.4rem;
    text-align: center;
    color: #64748b;
    font-size: 0.75rem;
    background: rgba(15, 23, 42, 0.4);
}

/* Operation log console */
.algo-log-box {
    background: #090d16;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 0.75rem;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 0.82rem;
    color: #38bdf8;
    line-height: 1.5;
    max-height: 240px;
    overflow-y: auto;
}

.receipt-card {
    background: #1e293b;
    border: 1px solid #3b82f6;
    border-radius: 10px;
    padding: 1.25rem;
    margin-top: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}
</style>
"""

VEHICLE_ICONS = {
    "Sedan": "🚗",
    "SUV": "🚙",
    "EV": "⚡",
    "Truck": "🚚",
    "Motorcycle": "🏍️",
    "Van": "🚐"
}

def render_vehicle_card(vehicle, depth: int, is_top: bool = False) -> str:
    icon = VEHICLE_ICONS.get(vehicle.vehicle_type, "🚗")
    top_badge = '<span style="color:#22c55e; font-weight:700; font-size:0.7rem;">[EXIT READY]</span>' if is_top else f'<span style="color:#94a3b8; font-size:0.7rem;">Depth: {depth}</span>'
    card_class = "vehicle-card top-vehicle-card" if is_top else "vehicle-card"

    return f"""
    <div class="{card_class}" style="border-left-color: {vehicle.color};">
        <div class="vehicle-header">
            <span class="plate-badge">{icon} {vehicle.plate}</span>
            {top_badge}
        </div>
        <div class="vehicle-meta">
            <span>👤 {vehicle.owner}</span>
            <span class="type-tag">{vehicle.vehicle_type}</span>
        </div>
        <div class="vehicle-meta" style="font-size: 0.7rem; color: #64748b;">
            <span>⏱️ {vehicle.entry_time.strftime('%H:%M:%S')}</span>
            <span>₹{vehicle.rate_per_hour:.2f}/hr</span>
        </div>
    </div>
    """

def render_empty_slot(slot_index: int) -> str:
    return f"""
    <div class="empty-slot">
        <span>EMPTY SLOT #{slot_index}</span>
    </div>
    """
