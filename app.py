import streamlit as st
import plotly.graph_objects as go
import pyttsx3
import random
import time
from datetime import datetime

# --- 1. INDUSTRIAL SCADA THEME SETUP ---
st.set_page_config(page_title="Intelligent Power Panel", layout="wide")

# Inject custom CSS to replicate the exact look and feel of your HTML file
st.markdown("""
    <style>
        /* Base Page Background */
        .stApp {
            background-color: #0a0e1a !important;
            color: #f9fafb !important;
        }
        
        /* Custom Header Styling */
        .scada-header {
            background: linear-gradient(135deg, #111827 0%, #1a1f2e 100%);
            border-bottom: 2px solid #3b82f6;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .scada-title {
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }
        
        /* Panel Container boxes */
        div[data-testid="stVerticalBlock"] > div {
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 10px;
        }
        
        /* Metric Card Text overrides */
        div[data-testid="stMetricValue"] {
            font-family: 'Courier New', monospace;
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #f9fafb !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #9ca3af !important;
            font-size: 13px !important;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize offline voice engine
engine = pyttsx3.init()

# --- 2. HMI VOICE LOGIC ---
def speak_status(load_type, currents, temps):
    if load_type == "Single-Phase System":
        status_text = f"System check. Single phase load active. Current is {currents[0]} Amps. Breaker temperature is {temps[0]} degrees Celsius."
    else:
        status_text = f"System check. Three phase load active. Maximum breaker temperature is {max(temps)} degrees Celsius."
    engine.say(status_text)
    engine.runAndWait()

# --- 3. PLOTLY GRAPH & GAUGE ENGINES ---
def draw_scada_gauge(value, title, unit, bar_color, max_val=60):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14, 'color': "#9ca3af"}},
        number={'suffix': f" {unit}", 'font': {'size': 18, 'color': "#f9fafb"}, 'font_family': "Courier New"},
        gauge={
            'axis': {'range': [0, max_val], 'tickwidth': 1, 'tickcolor': "#374151"},
            'bar': {'color': bar_color},
            'steps': [
                {'range': [0, max_val * 0.75], 'color': "#1f2937"},
                {'range': [max_val * 0.75, max_val], 'color': "#ef4444"}
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        height=140, margin=dict(l=10, r=10, t=25, b=10)
    )
    return fig

def draw_trend_chart(time_history, v_history, i_history):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_history, y=v_history, name="Voltage (V)", line=dict(color='#3b82f6', width=2)))
    fig.add_trace(go.Scatter(x=time_history, y=i_history, name="Current (A)", line=dict(color='#f59e0b', width=2), yaxis="y2"))
    
    fig.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        height=180, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        xaxis=dict(gridcolor="#374151", tickfont=dict(color="#9ca3af")),
        yaxis=dict(gridcolor="#374151", tickfont=dict(color="#3b82f6")),
        yaxis2=dict(tickfont=dict(color="#f59e0b"), overlaying="y", side="right")
    )
    return fig

# --- 4. DATA HISTORY STORAGE (For live graphing) ---
if "time_log" not in st.session_state:
    st.session_state.time_log = [datetime.now().strftime("%H:%M:%S") for _ in range(10)]
    st.session_state.v_log = [230.0 + random.uniform(-1, 1) for _ in range(10)]
    st.session_state.i_log = [14.0 + random.uniform(-2, 2) for _ in range(10)]

# --- 5. SCADA APP HEADER ---
st.markdown(f"""
    <div class="scada-header">
        <div class="scada-title">🔌 Intelligent Predictive Maintenance System</div>
        <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">
            Workstation Station Hub | Multi-Modal Sensor Fusion console
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 6. USER LOAD CONFIGURATION SELECTOR (YOUR COMPONENT MODIFICATION) ---
system_mode = st.selectbox(
    "🎛️ SELECT MEASUREMENT MODE FOR DATA PIPELINE:",
    ("3-Phase System", "Single-Phase System")
)
st.write("##")

# --- 7. TELEMETRY GENERATOR ---
current_time = datetime.now().strftime("%H:%M:%S")
v_L1 = round(random.uniform(228.5, 231.5), 1)
v_L2 = round(random.uniform(228.0, 231.0), 1) if system_mode == "3-Phase System" else 0.0
v_L3 = round(random.uniform(229.0, 232.0), 1) if system_mode == "3-Phase System" else 0.0

i_L1 = round(random.uniform(12.1, 16.5), 2)
i_L2 = round(random.uniform(11.8, 15.2), 2) if system_mode == "3-Phase System" else 0.0
i_L3 = round(random.uniform(13.0, 17.1), 2) if system_mode == "3-Phase System" else 0.0

# Temperature array per breaker (YOUR OTHER COMPONENT MODIFICATION)
t_L1 = round(random.uniform(32.0, 44.0), 1)
t_L2 = round(random.uniform(31.5, 42.5), 1) if system_mode == "3-Phase System" else 0.0
t_L3 = round(random.uniform(33.0, 49.0), 1) if system_mode == "3-Phase System" else 0.0
t_amb = round(random.uniform(24.0, 26.5), 1)

# Append data into rolling history logs
st.session_state.time_log.append(current_time)
st.session_state.v_log.append(v_L1)
st.session_state.i_log.append(i_L1)
# Keep logs locked to last 10 points
st.session_state.time_log = st.session_state.time_log[-10:]
st.session_state.v_log = st.session_state.v_log[-10:]
st.session_state.i_log = st.session_state.i_log[-10:]

# --- 8. RENDER INTERFACE GRID ---
# Top Row: Gauges
st.markdown("##### 📊 Current Transformer Telemetry Logs")
if system_mode == "3-Phase System":
    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(draw_scada_gauge(i_L1, f"L1 Current ({v_L1}V)", "A", "#3b82f6"), use_container_width=True)
    with g2: st.plotly_chart(draw_scada_gauge(i_L2, f"L2 Current ({v_L2}V)", "A", "#10b981"), use_container_width=True)
    with g3: st.plotly_chart(draw_scada_gauge(i_L3, f"L3 Current ({v_L3}V)", "A", "#f59e0b"), use_container_width=True)
else:
    g1, g2 = st.columns([2, 1])
    with g1: st.plotly_chart(draw_scada_gauge(i_L1, f"Main Current ({v_L1}V)", "A", "#3b82f6"), use_container_width=True)
    with g2: st.info("Single-Phase load validation sequence initiated. Phase lines L2 and L3 bypassed.")

# Middle Row: Breaker Point Temperatures (Replacing the thermal camera section)
st.markdown("##")
st.markdown("##### 🌡️ Contact Point Temperatures (Per Breaker Node)")
t1, t2, t3, t4 = st.columns(4)
with t1: st.metric(label="Breaker L1 Lug", value=f"{t_L1} °C", delta="Normal")
with t2: st.metric(label="Breaker L2 Lug", value=f"{t_L2} °C" if system_mode == "3-Phase System" else "OFFLINE")
with t3: st.metric(label="Breaker L3 Lug", value=f"{t_L3} °C" if system_mode == "3-Phase System" else "OFFLINE", delta="Hot Spot Warning" if t_L3 > 45 else None, delta_color="inverse")
with t4: st.metric(label="Panel Ambient", value=f"{t_amb} °C")

# Bottom Row: Analytical Trends and AI Actions
st.markdown("##")
left_panel, right_panel = st.columns([2, 1])

with left_panel:
    st.markdown("##### 📈 Real-Time Trend Analysis (Last 10 Cycles)")
    st.plotly_chart(draw_trend_chart(st.session_state.time_log, st.session_state.v_log, st.session_state.i_log), use_container_width=True)

with right_panel:
    st.markdown("##### 🤖 Automation & Voice HMI Actions")
    if (system_mode == "3-Phase System" and max(t_L1, t_L2, t_L3) > 45) or (system_mode == "Single-Phase System" and t_L1 > 45):
        st.error("⚠️ ANOMALY HIGH LOAD HEAT DETECTED")
    else:
        st.success("✅ Fault Classification Status: Nominal")
        
    if st.button("🔊 Trigger Audio Diagnostic Readout"):
        speak_status(system_mode, [i_L1, i_L2, i_L3], [t_L1, t_L2, t_L3])

# Auto rerun refresh ticker
time.sleep(2)
st.rerun()