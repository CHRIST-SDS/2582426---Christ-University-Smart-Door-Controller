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
    layout="wide"
)

# Custom CSS for Starlight / Wave Ride / Prussian Blue aesthetic
st.markdown("""
    <style>
    /* Global background and text styling */
    .main {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    stApp {
        background-color: #0d1b2a;
    }
    
    /* Header Styling */
    h1, h2, h3 {
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
        font-size: 2.8rem;
        font-weight: bold;
        color: #77abb7;
        margin: 5px 0;
    }
    
    .date-display {
        font-size: 1.1rem;
        color: #e0e1dd;
        opacity: 0.8;
    }

    /* Table styling - Clean transparent look */
    .stDataFrame {
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. AUTO-REFRESH & LIVE IST TIME
# ---------------------------------------------------------
# Auto-refresh app every 1 second (1000ms) for real-time clock and status updates
st_autorefresh(interval=1000, key="gate_clock_refresh")

# Fetch current time in IST
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

current_time_str = now.strftime("%I:%M:%S %p")
current_date_str = now.strftime("%A, %b %d, %Y")

# ---------------------------------------------------------
# 3. HEADER & CONTROL PANEL
# ---------------------------------------------------------
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

# Determine Gate Status based on 10-minute class window logic (Example: 09:00 - 09:10 AM)
# Adjust hour/minute conditions as per your campus schedule rules
current_minute = now.minute
current_hour = now.hour

# Example Logic: Open for first 10 minutes of the hour, restricted afterwards
is_gate_open = current_minute <= 10

with col_status:
    status_title = "GATE OPEN" if is_gate_open else "RESTRICTED ACCESS"
    status_color = "#2a9d8f" if is_gate_open else "#e76f51"
    status_desc = "Normal Entry Window Active" if is_gate_open else "Late Entry — AI Policy Applied"

    st.markdown(f"""
        <div class="status-card" style="border-left: 6px solid {status_color};">
            <h3>Gate Operational Status</h3>
            <div style="font-size: 2rem; font-weight: bold; color: {status_color}; margin: 10px 0;">
                {status_title}
            </div>
            <p>{status_desc}</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. POLICY & LOGS SECTION
# ---------------------------------------------------------
st.markdown("### 📋 Access Policies & Log View")

policy_data = {
    "Rule ID": ["POL-01", "POL-02", "POL-03"],
    "Condition": ["On Time (0-10 mins)", "Grace Period (10-15 mins)", "Late Entry (>15 mins)"],
    "Action": ["Automated Unlatch", "Log Reason & Notify", "Security Approval Required"],
    "Priority": ["Normal", "Medium", "High"]
}

df_policy = pd.DataFrame(policy_data)
st.table(df_policy)