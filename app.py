import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Smart Gate Controller",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Starlight / Wave Ride / Prussian Blue aesthetic
st.markdown("""
    <style>
    /* Global Background and Container Styling */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #0d1b2a !important;
        color: #e0e1dd !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1b263b !important;
        border-right: 1px solid #415a77;
    }
    [data-testid="stSidebar"] * {
        color: #e0e1dd !important;
    }

    /* Header & Text Visibility */
    h1, h2, h3, h4, h5, h6, span, label {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Card / Container Styling */
    .status-card {
        background-color: #1b263b;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid #415a77;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Metric / Clock Display */
    .clock-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #77abb7;
        margin: 5px 0;
    }
    
    .date-display {
        font-size: 1.1rem;
        color: #e0e1dd;
        opacity: 0.8;
    }

    /* Table Styling for Dark Background */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #1b263b !important;
        border-radius: 8px;
    }
    table {
        color: #e0e1dd !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. AUTO-REFRESH & LIVE IST TIME
# ---------------------------------------------------------
# Auto-refresh every 1 second (1000ms) for real-time system clock
st_autorefresh(interval=1000, key="gate_clock_refresh")

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

current_time_str = now.strftime("%I:%M:%S %p")
current_date_str = now.strftime("%A, %b %d, %Y")

# ---------------------------------------------------------
# 3. SIDEBAR NAVIGATION & CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.title("🚪 Navigation")
    st.markdown("---")
    
    page = st.radio(
        "Select Panel",
        ["Dashboard", "Access Logs", "System Settings"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("⚙️ System Override")
    manual_override = st.toggle("Force Gate Open", value=False)
    
    st.markdown("---")
    st.caption("AI Smart Gate Controller v2.1")
    st.caption("Environment: Streamlit Cloud (IST)")

# ---------------------------------------------------------
# 4. MAIN DASHBOARD VIEW
# ---------------------------------------------------------
if page == "Dashboard":
    st.title("🚪 Campus Smart Gate Controller")
    st.markdown("---")

    col_time, col_status = st.columns([1, 1])

    with col_time:
        st.markdown(f"""
            <div class="status-card">
                <h3>Campus Control Panel</h3>
                <p style="margin-bottom: 0px; opacity: 0.7;">Live System Time (IST)</p>
                <div class="clock-display">{current_time_str}</div>
                <div class="date-display">{current_date_str}</div>
            </div>
        """, unsafe_allow_html=True)

    # 10-minute class entry logic OR manual override
    current_minute = now.minute
    is_gate_open = manual_override or (current_minute <= 10)

    with col_status:
        status_title = "GATE OPEN" if is_gate_open else "RESTRICTED ACCESS"
        status_color = "#2a9d8f" if is_gate_open else "#e76f51"
        status_desc = "Manual Override Enabled" if manual_override else ("Normal Entry Window Active" if is_gate_open else "Late Entry — AI Policy Applied")

        st.markdown(f"""
            <div class="status-card" style="border-left: 6px solid {status_color};">
                <h3>Gate Operational Status</h3>
                <div style="font-size: 2rem; font-weight: bold; color: {status_color}; margin: 10px 0;">
                    {status_title}
                </div>
                <p>{status_desc}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📋 Access Policies & Guidelines")

    policy_data = {
        "Rule ID": ["POL-01", "POL-02", "POL-03"],
        "Condition": ["On Time (0-10 mins)", "Grace Period (10-15 mins)", "Late Entry (>15 mins)"],
        "Action": ["Automated Unlatch", "Log Reason & Notify", "Security Approval Required"],
        "Priority": ["Normal", "Medium", "High"]
    }

    df_policy = pd.DataFrame(policy_data)
    st.table(df_policy)

elif page == "Access Logs":
    st.title("📑 System Access Logs")
    st.markdown("---")
    
    # Sample logs table
    logs_data = {
        "Timestamp": [now.strftime("%Y-%m-%d %H:%M:%S")],
        "User ID": ["STU-82426"],
        "Access Status": ["Granted" if is_gate_open else "Flagged"],
        "Gate Mode": ["Automated"]
    }
    st.dataframe(pd.DataFrame(logs_data), use_container_width=True)

elif page == "System Settings":
    st.title("⚙️ Controller Settings")
    st.markdown("---")
    st.text_input("Server Timezone", value="Asia/Kolkata (IST)", disabled=True)
    st.slider("Door Unlatch Duration (Seconds)", min_value=3, max_value=15, value=5)