import streamlit as st
import plotly.graph_objects as go
import pyttsx3
import random
import time

# --- 1. DASHBOARD CONFIGURATION ---
st.set_page_config(page_title="Intelligent Power Monitor", layout="wide")
engine = pyttsx3.init()

# --- 2. VOICE ASSISTANT FUNCTION ---
def speak_status(p1, p2, p3, temp):
    status_text = f"System check. Phase 1 is {p1} Amps. Phase 2 is {p2} Amps. Phase 3 is {p3} Amps. Thermal sensor reads {temp} degrees Celsius."
    engine.say(status_text)
    engine.runAndWait()

# --- 3. DYNAMIC GAUGE CREATOR ---
def draw_industrial_gauge(value, title, max_value, unit, bar_color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': "white"}},
        number={'suffix': f" {unit}", 'font': {'size': 24, 'color': "white"}},
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': bar_color},
            'steps': [
                {'range': [0, max_value * 0.75], 'color': "#2b2b2b"},
                {'range': [max_value * 0.75, max_value], 'color': "#b22222"} # Warning Threshold Zone
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="#1e1e1e", # Sleek dark theme matching your tech setup
        plot_bgcolor="#1e1e1e",
        height=250,
        margin=dict(l=30, r=30, t=40, b=10)
    )
    return fig

# --- 4. HEADER INTERFACE ---
st.title("⚡ Intelligent Predictive Maintenance System")
st.markdown("### 3-Phase Power Panel Diagnostics Console")
st.write("---")

# --- 5. GENERATING MOCK SENSOR DATA ---
# (Tonight we simulate, tomorrow we switch this to the ESP32 Serial reading)
p1_current = round(random.uniform(11.5, 14.8), 2)
p2_current = round(random.uniform(10.2, 13.9), 2)
p3_current = round(random.uniform(12.1, 15.2), 2)
panel_temp = round(random.uniform(31.0, 48.0), 1) # Simulating shifting temperatures

# --- 6. DISPLAY LAYOUT ---
# Row 1: 3-Phase Amperage Gauges
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(draw_industrial_gauge(p1_current, "Phase 1 Current", 30, "A", "#1f77b4"), use_container_width=True)
with col2:
    st.plotly_chart(draw_industrial_gauge(p2_current, "Phase 2 Current", 30, "A", "#2ca02c"), use_container_width=True)
with col3:
    st.plotly_chart(draw_industrial_gauge(p3_current, "Phase 3 Current", 30, "A", "#ff7f0e"), use_container_width=True)

st.write("---")

# Row 2: MLX90614 Thermal Metrics & Voice Actions
left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader("🌡️ Panel Thermal Diagnostics")
    st.metric(label="MLX90614 Contactless IR Temperature", value=f"{panel_temp} °C")
    
    # Simple predictive alert rule
    if panel_temp > 45.0:
        st.error("⚠️ PREDICTIVE FAULT ALERT: High thermal anomaly detected on connector busbars!")
    else:
        st.success("✅ Thermal status within nominal parameters.")

with right_panel:
    st.subheader("🎙️ Interactive HMI Actions")
    st.write("Trigger system diagnostic audio announcement over local control workstation speakers:")
    if st.button("🔊 Execute Voice Status Readout"):
        speak_status(p1_current, p2_current, p3_current, panel_temp)

# --- 7. AUTO-REFRESH SYSTEM ---
time.sleep(2)
st.rerun()
