import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Smart Gate Controller",
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
    
    .date-display {
        font-size: 1.8rem;
        font-weight: bold;
        color: #77abb7;
        margin-top: 10px;
    }

    /* Table styling - Clean transparent look */
    .stDataFrame {
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATE CALCULATION
# ---------------------------------------------------------
current_date_str = datetime.now().strftime("%A, %B %d, %Y")

# ---------------------------------------------------------
# 3. HEADER & CONTROL PANEL
# ---------------------------------------------------------
st.title("Campus Smart Gate Controller")
st.markdown("---")

col_info, col_status = st.columns([1, 1])

with col_info:
    st.markdown(f"""
        <div class="status-card">
            <h3>Campus Control Panel</h3>
            <p style="margin-bottom: 0px; opacity: 0.7;">System Date</p>
            <div class="date-display">{current_date_str}</div>
        </div>
    """, unsafe_allow_html=True)

# Operational status flag
is_gate_open = True

with col_status:
    status_title = "GATE OPEN" if is_gate_open else "RESTRICTED ACCESS"
    status_color = "#2a9d8f" if is_gate_open else "#e76f51"
    status_desc = "Normal Entry Active" if is_gate_open else "AI Policy Applied"

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
st.markdown("### Access Policies and Log View")

policy_data = {
    "Rule ID": ["POL-01", "POL-02", "POL-03"],
    "Condition": ["On Time Entry", "Grace Period Entry", "Late Entry"],
    "Action": ["Automated Unlatch", "Log Reason and Notify", "Security Approval Required"],
    "Priority": ["Normal", "Medium", "High"]
}

df_policy = pd.DataFrame(policy_data)
st.table(df_policy)