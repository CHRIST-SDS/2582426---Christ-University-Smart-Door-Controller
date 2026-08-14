import streamlit as st
import os
from src.llm_engine import process_door_command
from src.image_engine import generate_status_badge

# Ensure output directory exists
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="UniAccess AI - Smart Entrance Control", layout="wide")

st.title("🚪 UniAccess AI: Gen-AI Campus Gatekeeper")
st.caption("100% Offline Local Architecture powered by Llama 3 & Local SDXL Turbo")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Gate Control Command (LLM)")
    selected_block = st.selectbox("Select Campus Block", ["Block 1", "Block 2", "Block 3", "Block 4"])
    user_prompt = st.text_area(
        "Enter Command / Request", 
        "Extend attendance gate window by 10 minutes for Block 2 due to a delayed guest lecture."
    )
    
    if st.button("Execute Gate Command", type="primary"):
        with st.spinner("Processing decision with local Llama 3..."):
            log_output = process_door_command(user_prompt, selected_block)
            st.success("Decision Processed & Logged!")
            st.markdown("### 🤖 Security Controller Log:")
            st.info(log_output)
            st.session_state['latest_status'] = f"{selected_block} - Access Granted"

with col2:
    st.header("2. Security Visual Badge (Local Image Gen)")
    if 'latest_status' in st.session_state:
        st.write(f"**Current Active Status:** `{st.session_state['latest_status']}`")
        if st.button("Generate Security Pass"):
            with st.spinner("Generating visual pass with local SDXL-Turbo..."):
                img_path = generate_status_badge(st.session_state['latest_status'])
                st.image(img_path, caption="Live Generated Security Gate Badge", use_container_width=True)
    else:
        st.write("👈 Submit a gate command on the left panel first to generate a security pass.")