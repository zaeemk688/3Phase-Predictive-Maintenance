import streamlit as st
import time
import random
from database_manager import log_telemetry, save_blackbox_emergency
from server import PredictiveMaintenanceAI
from voice_assistant import PanelVoiceAssistant

# Initialize Core AI Brain and Voice Synthesizer
@st.cache_resource
def initialize_core_modules():
    return PredictiveMaintenanceAI(), PanelVoiceAssistant()

ai_brain, voice = initialize_core_modules()

# ==========================================
# UI HEADER & THEMING
# ==========================================
st.set_page_config(page_title="Industrial Panel AI Dashboard", page_icon="⚡", layout="wide")
st.title("⚡ Intelligent Predictive Maintenance Panel Dashboard")
st.markdown("---")

# ==========================================
# SIDEBAR CONFIGURATION LAYER (BLOCK 1)
# ==========================================
st.sidebar.header("🛡️ System Control Matrix")

# User Authentication Matrix display placeholder
st.sidebar.info("Current Session Role: **Admin**")

# Pre-Start Phase Configuration Toggle Switch
system_mode = st.sidebar.radio(
    "Select Panel Deployment Configuration:",
    options=["Single-Phase Monitoring", "Three-Phase Monitoring"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Protection Parameter Limits")
safe_voltage_max = st.sidebar.slider("Max Voltage Limit (V)", 240, 260, 245)
safe_current_max = st.sidebar.slider("Max Current Limit (A)", 15, 60, 30)

# Start button to control tracking execution loops
run_panel = st.sidebar.checkbox("Activate Real-Time Panel Scan", value=False)

# ==========================================
# LIVE METRICS LAYOUT (BLOCK 6)
# ==========================================
# Creating placeholders for live updating data blocks
metric_slots = st.empty()
status_box = st.empty()

if run_panel:
    st.sidebar.success("🟢 System scanning is live...")
    
    # Execution simulation loop (This later binds to your main_engine script)
    while run_panel:
        # Simulate data streaming from the hardware block
        smoke_raw = random.randint(150, 220)
        flame_tripped = False
        temp_reading = random.uniform(28.0, 36.0)
        
        # Branch variables based on selected Phase Mode
        if "Three-Phase" in system_mode:
            voltages = [random.randint(218, 224) for _ in range(3)] + [0, 0, 0]
            currents = [random.randint(8, 14) for _ in range(3)] + [0, 0, 0]
            v_avg = sum(voltages[:3]) / 3.0
            v_unbalance = random.uniform(0.2, 1.2)
            c_max = max(currents[:3])
            pf = random.uniform(0.91, 0.96)
            thd = random.uniform(1.8, 3.2)
        else:
            voltages = [random.randint(215, 225)] + [0]*5
            currents = [random.randint(12, 18)] + [0]*5
            v_avg = voltages[0]
            v_unbalance = 0.0
            c_max = currents[0]
            pf = random.uniform(0.88, 0.93)
            thd = random.uniform(2.0, 3.5)

        # ------------------------------------------
        # AUTOMATED PROTECTION & CRITICAL TRIPS (BLOCK 5)
        # ------------------------------------------
        # Check single-phase safe limits if configured
        if "Single-Phase" in system_mode and (v_avg > safe_voltage_max or c_max > safe_current_max):
            status_box.error(f"🚨 CRITICAL TRIP: Parameter Limits Exceeded in Single Phase Mode!")
            voice.announce("Emergency trip. Safe operational parameter thresholds breached.", critical=True)
            save_blackbox_emergency("Safe Limit Breach", "Single-Phase Logic", smoke_raw, flame_tripped, voltages, currents, "Over-limit parameter trip")
            break

        # Send features directly into loaded Random Forest Classifier AI Models
        ai_diagnosis, confidence = ai_brain.predict_status(v_avg, v_unbalance, c_max, pf, thd, temp_reading)
        
        # Save telemetry frame to local database backend
        log_telemetry("Three" if "Three" in system_mode else "Single", smoke_raw, flame_tripped, voltages, currents)

        # Render updating UI layout components
        with metric_slots.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="Average Voltage", value=f"{v_avg:.1f} V")
            col2.metric(label="Peak Load Current", value=f"{c_max:.1f} A")
            col3.metric(label="True Power Factor", value=f"{pf:.2f}")
            col4.metric(label="Enclosure Temperature", value=f"{temp_reading:.1f} °C")

            col5, col6, col7 = st.columns(3)
            col5.metric(label="Total Harmonic Distortion (THD)", value=f"{thd:.2f} %")
            col6.metric(label="Voltage Phase Unbalance (PVUR)", value=f"{v_unbalance:.2f} %")
            col7.metric(label="Atmospheric Smoke Index", value=f"{smoke_raw}")

        with status_box.container():
            if "Normal" in ai_diagnosis:
                st.success(f"🧠 AI Panel Health Status: **{ai_diagnosis}** (Confidence: {confidence:.1f}%)")
            else:
                st.warning(f"⚠️ AI Panel Health Warning: **{ai_diagnosis}** (Confidence: {confidence:.1f}%)")
                voice.announce(f"Warning. {ai_diagnosis}")

        time.sleep(1.5) # Sample interval pause rate
else:
    st.info("💡 Dashboard Standing By. Check the 'Activate Real-Time Panel Scan' box on the sidebar menu to turn on telemetry loops.")