import re
import time
from collections import deque
from datetime import datetime

import pandas as pd
import plotly.express as px
import serial
from serial.tools import list_ports
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# -------------------- Page setup --------------------
st.set_page_config(
    page_title="Smart Irrigation Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background: #0b1220; color: #e5e7eb; }
    [data-testid="stSidebar"] { background: #111b2e; }
    [data-testid="stMetric"] {
        background: #142238; border: 1px solid #263a56;
        padding: 16px; border-radius: 14px;
    }
    div.stButton > button {
        border-radius: 10px; min-height: 2.7rem; font-weight: 600;
    }
    .small-muted { color: #91a4bd; font-size: 0.88rem; }
    .status-pill {
        display:inline-block; padding:5px 11px; border-radius:20px;
        font-size:0.82rem; font-weight:700; background:#173d32; color:#6ee7b7;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Smart Irrigation System")
st.caption("LIVE MONITORING  •  ARDUINO NANO  •  USB SERIAL")

# -------------------- Session state --------------------
if "ser" not in st.session_state:
    st.session_state.ser = None
if "serial_buffer" not in st.session_state:
    st.session_state.serial_buffer = b""
if "readings" not in st.session_state:
    st.session_state.readings = deque(maxlen=180)
if "last_value" not in st.session_state:
    st.session_state.last_value = None
if "last_seen" not in st.session_state:
    st.session_state.last_seen = None
if "system_message" not in st.session_state:
    st.session_state.system_message = "Not connected"
if "watering_command" not in st.session_state:
    st.session_state.watering_command = "Unknown"
if "connection_error" not in st.session_state:
    st.session_state.connection_error = ""

# -------------------- Sidebar connection settings --------------------
st.sidebar.header("Connection settings")
available_ports = [p.device for p in list_ports.comports()]
default_port = "COM9" if "COM9" in available_ports else (available_ports[0] if available_ports else "COM9")
port_options = list(dict.fromkeys(available_ports + [default_port]))
selected_port = st.sidebar.selectbox(
    "Serial port", port_options,
    index=port_options.index(default_port) if default_port in port_options else 0
)
baud_rate = st.sidebar.selectbox("Baud rate", [9600, 19200, 38400, 57600, 115200], index=0)
st.sidebar.caption("The baud rate must match Serial.begin(...) in your Arduino sketch.")

connected = st.session_state.ser is not None and st.session_state.ser.is_open
if not connected:
    if st.sidebar.button("Connect to Arduino", type="primary", use_container_width=True):
        try:
            st.session_state.ser = serial.Serial(selected_port, baud_rate, timeout=0)
            time.sleep(2)  # Arduino Nano may reset when its serial port opens
            st.session_state.ser.reset_input_buffer()
            st.session_state.serial_buffer = b""
            st.session_state.connection_error = ""
            st.session_state.system_message = "Connected — waiting for sensor data"
            st.rerun()
        except Exception as exc:
            st.session_state.ser = None
            st.session_state.connection_error = str(exc)
else:
    st.sidebar.success(f"Connected to {st.session_state.ser.port}")
    if st.sidebar.button("Disconnect", use_container_width=True):
        try:
            st.session_state.ser.close()
        except Exception:
            pass
        st.session_state.ser = None
        st.session_state.system_message = "Disconnected"
        st.rerun()

if st.session_state.connection_error:
    st.sidebar.error(f"Connection failed: {st.session_state.connection_error}")

st.sidebar.divider()
st.sidebar.markdown("**Serial commands**")
st.sidebar.code("1  → Activate automatic watering\n0  → Deactivate system", language="text")
st.sidebar.caption("This dashboard sends the same 1/0 commands as your Serial Monitor.")

# -------------------- Read serial data --------------------
ser = st.session_state.ser
if ser is not None and ser.is_open:
    try:
        waiting = ser.in_waiting
        if waiting:
            st.session_state.serial_buffer += ser.read(waiting)
        while b"\n" in st.session_state.serial_buffer:
            raw_line, st.session_state.serial_buffer = st.session_state.serial_buffer.split(b"\n", 1)
            line = raw_line.decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            now = datetime.now()
            st.session_state.last_seen = now

            moisture_match = re.search(r"Soil\s*Moisture\s*Level\s*:\s*(-?\d+)", line, re.IGNORECASE)
            if moisture_match:
                value = int(moisture_match.group(1))
                st.session_state.last_value = value
                st.session_state.readings.append({
                    "Time": now,
                    "Soil moisture (raw)": value
                })

            if "system activated" in line.lower():
                st.session_state.system_message = "System activated"
                st.session_state.watering_command = "Automatic watering ON"
            elif "deactivated" in line.lower():
                st.session_state.system_message = "System deactivated"
                st.session_state.watering_command = "Automatic watering OFF"
            elif "monitoring soil" in line.lower():
                st.session_state.system_message = "Monitoring soil"
    except Exception as exc:
        st.session_state.connection_error = str(exc)

# Refresh page periodically to collect incoming serial data
st_autorefresh(interval=1000, key="serial_dashboard_refresh")

# -------------------- Status header --------------------
connected = st.session_state.ser is not None and st.session_state.ser.is_open
status_col, info_col = st.columns([1, 3])
with status_col:
    if connected:
        st.markdown('<span class="status-pill">● ARDUINO CONNECTED</span>', unsafe_allow_html=True)
    else:
        st.error("● ARDUINO DISCONNECTED")
with info_col:
    st.markdown(
        '<div class="small-muted">Select the correct COM port and baud rate in the sidebar, then connect.</div>',
        unsafe_allow_html=True
    )

# -------------------- Main metrics --------------------
m1, m2, m3 = st.columns(3)
with m1:
    value = st.session_state.last_value
    st.metric("Soil moisture reading", f"{value}" if value is not None else "—", help="Raw analog value received from Arduino (commonly 0–1023).")
with m2:
    st.metric("System message", st.session_state.system_message)
with m3:
    last_seen = st.session_state.last_seen
    st.metric("Last data received", last_seen.strftime("%H:%M:%S") if last_seen else "—")

st.caption("Sensor values are shown as raw readings. A moisture percentage needs dry-soil and wet-soil calibration.")

# -------------------- Controls --------------------
st.subheader("Watering controls")
left, right = st.columns(2)
with left:
    if st.button("▶  ACTIVATE AUTOMATIC WATERING", type="primary", use_container_width=True, disabled=not connected):
        try:
            st.session_state.ser.write(b"1")
            st.session_state.watering_command = "Activation command sent"
            st.toast("Activation command sent to Arduino")
        except Exception as exc:
            st.error(f"Could not send command: {exc}")
with right:
    if st.button("■  DEACTIVATE SYSTEM", use_container_width=True, disabled=not connected):
        try:
            st.session_state.ser.write(b"0")
            st.session_state.watering_command = "Deactivation command sent"
            st.toast("Deactivation command sent to Arduino")
        except Exception as exc:
            st.error(f"Could not send command: {exc}")

st.info(f"Last control state: **{st.session_state.watering_command}**")

# -------------------- Live chart --------------------
st.subheader("Live soil moisture history")
if st.session_state.readings:
    df = pd.DataFrame(list(st.session_state.readings))
    fig = px.line(
        df, x="Time", y="Soil moisture (raw)",
        markers=True, template="plotly_dark",
        title="Soil sensor readings"
    )
    fig.update_layout(
        paper_bgcolor="#0b1220", plot_bgcolor="#111b2e",
        font_color="#e5e7eb", margin=dict(l=10, r=10, t=50, b=10),
        height=360, xaxis_title="Time", yaxis_title="Raw sensor value"
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=5))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No sensor readings received yet. Connect the Arduino and confirm that its Serial Monitor output includes lines such as: Soil Moisture Level: 1023")

# -------------------- Recent data --------------------
with st.expander("Recent sensor readings"):
    if st.session_state.readings:
        recent = pd.DataFrame(list(st.session_state.readings)).tail(20).iloc[::-1]
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.write("No readings available yet.")

st.divider()
st.caption("Smart Irrigation Dashboard • Local laptop application • Data is read directly from the Arduino USB serial connection.")
