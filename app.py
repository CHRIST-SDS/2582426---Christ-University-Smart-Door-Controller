import streamlit as st
import pandas as pd
import os
from datetime import datetime
from src.llm_engine import process_gate_command
from src.image_engine import get_door_image

# Auto-refresh every 10 seconds for real-time synchronization
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=10000, key="datarefresh")
except ImportError:
    pass

# Page configuration
st.set_page_config(
    page_title="Christ University Smart Door Controller",
    layout="wide"
)

# ==========================================
# CUSTOM CSS: STARLIGHT, WAVE RIDE & PRUSSIAN BLUE
# ==========================================
st.markdown("""
    <style>
    /* Main App Background - Starlight Blue */
    .stApp {
        background-color: #BED6E0;
        color: #003153;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling - Prussian Blue */
    section[data-testid="stSidebar"] {
        background-color: #003153;
        color: #BED6E0;
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* Custom Styled Cards for Sidebar Blocks */
    .block-card {
        background: linear-gradient(135deg, #003153 0%, #3B8AB1 100%);
        border: 1.5px solid #3B8AB1;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 49, 83, 0.25);
    }
    
    .block-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 15px;
    }
    
    .status-badge-open {
        background-color: #BED6E0;
        color: #003153;
        font-weight: 700;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    .status-badge-closed {
        background-color: #3B8AB1;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    /* Main Top-Level Dashboard Column Cards ONLY */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 14px;
        border: 2px solid #3B8AB1;
        box-shadow: 0 6px 16px rgba(0, 49, 83, 0.12);
    }

    /* Keep inner/nested alignment columns transparent (removes red-circled side boxes) */
    div[data-testid="stColumn"] div[data-testid="stColumn"] {
        background-color: transparent !important;
        padding: 0px !important;
        border: none !important;
        box-shadow: none !important;
    }

    .center-heading {
        text-align: center;
        color: #003153;
        font-weight: 700;
        margin-bottom: 16px;
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox select {
        border-radius: 8px !important;
        border: 1.5px solid #3B8AB1 !important;
        background-color: #FFFFFF !important;
        color: #003153 !important;
    }
    
    /* Primary Action Buttons */
    .stButton > button {
        background-color: #003153 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #3B8AB1 !important;
        color: #FFFFFF !important;
    }
    
    /* Alert Banners */
    .stAlert {
        background-color: #FFFFFF !important;
        color: #003153 !important;
        border: 1.5px solid #3B8AB1 !important;
        border-radius: 10px !important;
    }

    /* ==========================================
       CUSTOM 3D TIMETABLE STYLING (CLEAN TEXT)
       ========================================== */
    .timetable-wrapper {
        background: #FFFFFF;
        border-radius: 14px;
        border: 2px solid #3B8AB1;
        box-shadow: 0 8px 24px rgba(0, 49, 83, 0.15);
        overflow: hidden;
        margin-top: 10px;
    }

    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-family: 'Inter', sans-serif;
    }

    /* Highlighted Table Header */
    .custom-table th {
        background: linear-gradient(135deg, #003153 0%, #0A4174 100%);
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        text-align: left;
        padding: 16px 20px;
        letter-spacing: 0.5px;
        border-bottom: 3px solid #3B8AB1;
    }

    /* Table Body Cells */
    .custom-table td {
        padding: 14px 20px;
        font-size: 14px;
        color: #003153;
        border-bottom: 1px solid #BED6E0;
        transition: all 0.25s ease-in-out;
    }

    /* Alternating Row Colors */
    .custom-table tbody tr:nth-child(even) {
        background-color: #F8FCFD;
    }
    .custom-table tbody tr:nth-child(odd) {
        background-color: #FFFFFF;
    }

    /* Hover & 3D Lift Effect */
    .custom-table tbody tr {
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
    }

    .custom-table tbody tr:hover {
        background-color: #BED6E0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 49, 83, 0.18);
        cursor: pointer;
    }

    /* Clean Policy Text Colors */
    .policy-locked {
        color: #003153;
        font-weight: 700;
        font-size: 14px;
    }

    .policy-open {
        color: #3B8AB1;
        font-weight: 600;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Block Statuses
if "block_statuses" not in st.session_state:
    st.session_state["block_statuses"] = {
        "Block 1": "CLOSED",
        "Block 2": "CLOSED",
        "Block 3": "CLOSED",
        "Block 4": "CLOSED"
    }

# ==========================================
# SIDEBAR: Live Time & Block Cards
# ==========================================
with st.sidebar:
    st.title("Campus Control Panel")
    
    # Real-Time Clock Display
    now = datetime.now()
    st.metric("Live System Time", now.strftime("%I:%M:%S %p"))
    st.caption(f"Date: {now.strftime('%A, %b %d, %Y')}")
    st.markdown("---")
    
    st.subheader("Live Gate Status")
    
    # Render Custom Block Status Cards
    for b_name, b_status in st.session_state["block_statuses"].items():
        badge_class = "status-badge-open" if b_status == "OPEN" else "status-badge-closed"
        st.markdown(
            f"""
            <div class="block-card">
                <span class="block-title">{b_name}</span>
                <span class="{badge_class}">{b_status}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# HERO BANNER SECTION
# ==========================================
campus_img_path = os.path.join("data", "campus.png")
if not os.path.exists(campus_img_path):
    campus_img_path = os.path.join("data", "Campus.png")

if os.path.exists(campus_img_path):
    st.image(campus_img_path, use_container_width=True)

st.title("Christ University - AI Smart Door Controller")
st.markdown("---")

# ==========================================
# MAIN DASHBOARD - TOP SECTION
# ==========================================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Security Command Center")
    
    # Block Selection Dropdown
    selected_block = st.selectbox(
        "Select Target Campus Block:",
        ["Block 1", "Block 2", "Block 3", "Block 4"]
    )
    
    user_prompt = st.text_input(
        "Enter Gate Command:",
        value="open door for Period 1 start"
    )
    
    if st.button("Execute Gate Command", use_container_width=True):
        with st.spinner("Processing security command locally..."):
            decision = process_gate_command(user_prompt)
            st.session_state['last_command'] = user_prompt
            st.session_state['decision'] = decision
            
            # Update individual block status based on explicit command intent
            text_lower = user_prompt.lower()
            if any(w in text_lower for w in ["close", "lock", "shut", "deny"]):
                st.session_state["block_statuses"][selected_block] = "CLOSED"
            elif any(w in text_lower for w in ["open", "unlock", "grant", "allow"]):
                st.session_state["block_statuses"][selected_block] = "OPEN"

    # Display clean status update banner
    if 'decision' in st.session_state:
        status_text = st.session_state['block_statuses'][selected_block]
        st.success(f"Status Updated for {selected_block}: {status_text}")
        st.caption("Policy Rule Active: Automated 10-minute entry buffer enforced at start of class period.")

with col2:
    st.markdown('<h3 class="center-heading">Visual Status Tracker</h3>', unsafe_allow_html=True)
    
    if 'last_command' in st.session_state:
        door_image_path = get_door_image(st.session_state['last_command'])
        
        # Transparent sub-columns for center placement
        _, img_col, _ = st.columns([0.05, 1, 0.05])
        with img_col:
            st.image(
                door_image_path,
                caption=f"Physical Status: {selected_block} ({st.session_state['block_statuses'][selected_block]})",
                use_container_width=True
            )
    else:
        st.info("Submit a command on the left to view gate status.")

# ==========================================
# MAIN DASHBOARD - BOTTOM SECTION (3D TIMETABLE)
# ==========================================
st.markdown("---")
st.subheader("Gate Schedule Timetable & Real-Time Sync")
st.caption("Monday - Saturday | Hours: 08:30 AM - 04:30 PM (30-min Breaks Included)")

schedule_rows = [
    ("08:30 AM - 09:30 AM", "Period 1 (Class)", "Locked 08:30 - 08:40"),
    ("09:30 AM - 10:00 AM", "Morning Break (30m)", "Open Access"),
    ("10:00 AM - 11:00 AM", "Period 2 (Class)", "Locked 10:00 - 10:10"),
    ("11:00 AM - 12:00 PM", "Period 3 (Class)", "Locked 11:00 - 11:10"),
    ("12:00 PM - 01:00 PM", "Lunch Break (1h)", "Open Access"),
    ("01:00 PM - 02:00 PM", "Period 4 (Class)", "Locked 01:00 - 01:10"),
    ("02:00 PM - 02:30 PM", "Evening Break (30m)", "Open Access"),
    ("02:30 PM - 03:30 PM", "Period 5 (Class)", "Locked 02:30 - 02:40"),
    ("03:30 PM - 04:30 PM", "Period 6 (Class)", "Locked 03:30 - 03:40"),
]

# Generate Clean HTML Table Body
table_body = ""
for time_slot, event, policy in schedule_rows:
    badge_style = "policy-locked" if "Locked" in policy else "policy-open"
    table_body += f'<tr><td><strong>{time_slot}</strong></td><td>{event}</td><td><span class="{badge_style}">{policy}</span></td></tr>'

table_html = f"""<div class="timetable-wrapper">
<table class="custom-table">
<thead>
<tr>
<th>Time Slot</th>
<th>Schedule Event</th>
<th>Door Policy</th>
</tr>
</thead>
<tbody>
{table_body}
</tbody>
</table>
</div>"""

st.markdown(table_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.info("Note: Class doors automatically lock for the first 10 minutes of each lecture period before returning to automated access control.")