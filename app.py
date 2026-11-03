
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Mushroom Greenhouse",
    page_icon="🍄",
    layout="wide"
)

# HEADER
st.title("🍄 Mushroom Greenhouse Monitoring System")
st.write("IoT Environmental Monitoring Dashboard")
st.caption("Monitor temperature, air humidity and CO2 concentration.")

st.divider()

# SIDEBAR
st.sidebar.title("System Information")
st.sidebar.info("Mushroom Greenhouse Monitoring")

st.sidebar.subheader("Target Settings")

temp_min = st.sidebar.number_input(
    "Minimum Temperature (°C)", value=20.0
)
temp_max = st.sidebar.number_input(
    "Maximum Temperature (°C)", value=30.0
)

humidity_min = st.sidebar.number_input(
    "Minimum Air Humidity (%)", value=80.0
)
humidity_max = st.sidebar.number_input(
    "Maximum Air Humidity (%)", value=95.0
)

co2_min = st.sidebar.number_input(
    "Minimum CO2 (ppm)", value=400
)
co2_max = st.sidebar.number_input(
    "Maximum CO2 (ppm)", value=1500
)

# INITIAL DATA
if "readings" not in st.session_state:
    st.session_state.readings = [{
        "Time": datetime.now(),
        "Temperature": 25.0,
        "Humidity": 85.0,
        "CO2": 900
    }]


# LOAD BACKGROUND WALLPAPER

import base64
from pathlib import Path

image_path = Path(__file__).parent / "mushroom_bg.png"

if image_path.is_file():

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image:
                linear-gradient(
                    rgba(2, 25, 17, 0.65),
                    rgba(2, 25, 17, 0.78)
                ),
                url("data:image/png;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

else:
    st.error(f"Wallpaper not found: {image_path}")


# CUSTOM DESIGN: sensor cards, graph panel and dark-green information panels
st.markdown("""
<style>
.sensor-grid {
    display: flex;
    gap: 16px;
    margin: 12px 0 24px 0;
}
.sensor-card {
    flex: 1;
    min-width: 0;
    padding: 22px 20px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 5px 18px rgba(0,0,0,.22);
    border: 1px solid rgba(255,255,255,.18);
}
.sensor-card .sensor-name {
    font-size: 16px;
    font-weight: 650;
    opacity: .96;
}
.sensor-card .sensor-value {
    font-size: 32px;
    line-height: 1.35;
    font-weight: 750;
    margin-top: 8px;
}
.sensor-card .sensor-status {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .7px;
    margin-top: 5px;
}
.info-panel {
    background: #123d2b;
    color: #ffffff;
    padding: 22px;
    border-radius: 16px;
    margin: 12px 0 18px 0;
    border: 1px solid rgba(255,255,255,.12);
    box-shadow: 0 5px 18px rgba(0,0,0,.18);
}
.info-panel h3, .info-panel h4, .info-panel p,
.info-panel li, .info-panel strong {
    color: #ffffff !important;
}
.graph-panel {
    background: #ffffff;
    color: #1f2937;
    padding: 20px;
    border-radius: 16px;
    margin: 12px 0 20px 0;
    box-shadow: 0 5px 18px rgba(0,0,0,.18);
}
.graph-panel h3, .graph-panel p {
    color: #1f2937 !important;
}
.history-panel {
    background: #123d2b;
    color: #ffffff;
    padding: 20px;
    border-radius: 16px;
    margin: 12px 0 18px 0;
}
.history-panel h3, .history-panel p {
    color: #ffffff !important;
}
@media (max-width: 700px) {
    .sensor-grid { flex-direction: column; }
}
</style>
""", unsafe_allow_html=True)



# GENERATE NEW READING
st.markdown("""
<div style="
    background-color: #123D2B;
    color: white;
    padding: 15px 20px;
    border-radius: 12px;
">
    <h2 style="color:white; margin:0;">
        Current Monitoring
    </h2>
</div>
""", unsafe_allow_html=True)

if st.button("Generate New Sensor Reading"):

    new_data = {
        "Time": datetime.now(),
        "Temperature": round(random.uniform(20, 35), 1),
        "Humidity": round(random.uniform(65, 100), 1),
        "CO2": random.randint(400, 2500)
    }

    st.session_state.readings.append(new_data)

    st.session_state.readings = (
        st.session_state.readings[-100:]
    )

# LATEST DATA
df = pd.DataFrame(st.session_state.readings)
latest = df.iloc[-1]

temperature = latest["Temperature"]
humidity = latest["Humidity"]
co2 = latest["CO2"]

# SENSOR METRICS

# TEMPERATURE COLOUR
if temperature > temp_max:
    temp_color = "#DC2626"
    temp_status = "HOT / ABOVE TARGET"
else:
    temp_color = "#2563EB"
    temp_status = "NORMAL / COOL"

# HUMIDITY COLOUR
if humidity > humidity_max:
    humidity_color = "#DC2626"
    humidity_status = "HIGH / ABOVE TARGET"
else:
    humidity_color = "#2563EB"
    humidity_status = "NORMAL"

# CO2 COLOUR
if co2 > co2_max:
    co2_color = "#DC2626"
    co2_status = "HIGH / ABOVE TARGET"
else:
    co2_color = "#15803D"
    co2_status = "NORMAL"

# DISPLAY SENSOR BOXES
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background:{temp_color}; color:white;
    padding:25px; border-radius:15px; min-height:150px;">
        <h3 style="color:white;">🌡️ Temperature</h3>
        <h1 style="color:white;">{temperature:.1f} °C</h1>
        <b>{temp_status}</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:{humidity_color}; color:white;
    padding:25px; border-radius:15px; min-height:150px;">
        <h3 style="color:white;">💧 Air Humidity</h3>
        <h1 style="color:white;">{humidity:.1f} %</h1>
        <b>{humidity_status}</b>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:{co2_color}; color:white;
    padding:25px; border-radius:15px; min-height:150px;">
        <h3 style="color:white;">☁️ CO2 Concentration</h3>
        <h1 style="color:white;">{co2} ppm</h1>
        <b>{co2_status}</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# STATUS CHECK
st.subheader("")
def check_status(value, minimum, maximum):
    if minimum > maximum:
        return "Invalid target range"
    elif value < minimum:
        return "Below Target"
    elif value > maximum:
        return "Above Target"
    else:
        return "Within Target"

status1 = check_status(
    temperature, temp_min, temp_max
)

status2 = check_status(
    humidity, humidity_min, humidity_max
)

status3 = check_status(
    co2, co2_min, co2_max
)

st.markdown("""
<div style="background:#123D2B; color:white;
padding:15px 20px; border-radius:12px;">
<h2 style="color:white; margin:0;">
Environmental Status
</h2>
</div>
""", unsafe_allow_html=True)
st.divider()
col1, col2, col3 = st.columns(
    [1, 1, 1],
    gap="large"
)

with col1:
    st.markdown(f"""
    <div style="background:#123D2B; color:white;
    padding:20px; border-radius:12px;">
    <h3 style="color:white;">🌡️ Temperature</h3>
    <h4 style="color:white;">{status1}</h4>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#123D2B; color:white;
    padding:20px; border-radius:12px;">
    <h3 style="color:white;">💧 Air Humidity</h3>
    <h4 style="color:white;">{status2}</h4>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#123D2B; color:white;
    padding:20px; border-radius:12px;">
    <h3 style="color:white;">☁️ CO2</h3>
    <h4 style="color:white;">{status3}</h4>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# GRAPH — white background panel
st.markdown("""
<div style="background:#123D2B; color:white;
padding:15px 20px; border-radius:12px;">
<h2 style="color:white; margin:0;">
📈 Monitoring History
</h2>
</div>
""", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs([
    "Temperature",
    "Air Humidity",
    "CO2 Concentration"
])

if len(df) > 0:
    with tab1:
        fig1 = px.line(
            df, x="Time", y="Temperature", markers=True,
            title="Temperature (°C)"
        )
        fig1.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font_color="#1f2937", margin=dict(l=20, r=20, t=55, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.line(
            df, x="Time", y="Humidity", markers=True,
            title="Air Humidity (%)"
        )
        fig2.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font_color="#1f2937", margin=dict(l=20, r=20, t=55, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = px.line(
            df, x="Time", y="CO2", markers=True,
            title="CO2 Concentration (ppm)"
        )
        fig3.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            font_color="#1f2937", margin=dict(l=20, r=20, t=55, b=20)
        )
        st.plotly_chart(fig3, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="background:#123D2B; color:white;
padding:15px 20px; border-radius:12px;">
<h2 style="color:white; margin:0;">
🍄 Discover the World of Mushrooms
</h2>
</div>
""", unsafe_allow_html=True)
st.divider()
col1, col2= st.columns(
    [1, 1],
    gap="small"
)


with col1:
    st.markdown("""
<div style="background:#FFF3C4; color:#493B12;
padding:20px; border-radius:15px;">
<h3 style="color:#493B12;">💡 Did You Know?</h3>
Mushrooms are not plants!
They belong to the fungi kingdom.They obtain nutrients from
    organic materials in their growing environment.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#DDF3DF; color:#493B12;
padding:20px; border-radius:15px;margin-bottom:20px;">
<h3 style="color:#493B12;">🌱 Mushroom Growth</h3>
Environmental conditions are important for healthy mushroom growth.
Temperature, humidity and CO2 levels can influence mushroom development.
</div>
""", unsafe_allow_html=True)


with col2:
    st.markdown("""
<div style="background:#DCEEFF; color:#493B12;
padding:20px; border-radius:15px;">
<h3 style="color:#493B12;">🔬 Interesting Facts</h3>
Mushrooms reproduce through spores.
Mycelium is the network that grows through the growing substrate.
Some mushrooms can glow in the dark.
</div>
""", unsafe_allow_html=True)
   
    st.markdown("""
<div style="background:#EDE2FF; color:#493B12;
padding:20px; border-radius:15px;">
<h3 style="color:#493B12;">🌍 Environmental Benefits</h3>
Mushrooms help break down organic matter and recycle nutrients
in the environment.
</div>
""", unsafe_allow_html=True)

st.divider()

# WHY MONITOR YOUR MUSHROOM GREENHOUSE

st.markdown("""
<div style="
    background-color: #123D2B;
    color: white;
    padding: 15px 20px;
    border-radius: 12px;
">
    <h2 style="color:white; margin:0;">
        🌿 Why Monitor Your Mushroom Greenhouse?
    </h2>
</div>
""", unsafe_allow_html=True)
st.divider()
a, b, c = st.columns(3)

# BOX 1 - SOFT RED
with a:
    st.markdown("""
    <div style="
        background-color: #FADDDD;
        color: #642323;
        padding: 20px;
        border-radius: 15px;
        min-height: 160px;
    ">
        <h3 style="color:#642323;">
            🌡️ Better Environment
        </h3>
        Monitor temperature to maintain
        suitable growing conditions.
    </div>
    """, unsafe_allow_html=True)

# BOX 2 - SOFT ORANGE
with b:
    st.markdown("""
    <div style="
        background-color: #FFE7CC;
        color: #68401C;
        padding: 20px;
        border-radius: 15px;
        min-height: 160px;
    ">
        <h3 style="color:#68401C;">
            💧 Healthy Growth
        </h3>
        Monitor humidity to help prevent
        unsuitable conditions.
    </div>
    """, unsafe_allow_html=True)

# BOX 3 - SOFT YELLOW
with c:
    st.markdown("""
    <div style="
        background-color: #FFF3C4;
        color: #493B12;
        padding: 20px;
        border-radius: 15px;
        min-height: 160px;
    ">
        <h3 style="color:#493B12;">
            ☁️ CO2 Monitoring
        </h3>
        Track CO2 concentration to understand
        greenhouse ventilation.
    </div>
    """, unsafe_allow_html=True)
st.divider()

# SENSOR DATA HISTORY — dark-green panel
st.markdown('<div class="history-panel"><h3>📋 Sensor Data History</h3>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# DOWNLOAD CSV
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Sensor Data (CSV)",
    data=csv,
    file_name="mushroom_greenhouse_data.csv",
    mime="text/csv"
)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.caption(
    "Mushroom Greenhouse Monitoring System | EDP Project"
)

st.warning(
    "Demo version: All sensor readings are simulated, "
    "not collected from physical sensors."
)
