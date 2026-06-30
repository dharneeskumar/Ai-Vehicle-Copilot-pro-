import streamlit as st
import sys
import os
import cv2
import time

# =========================
# PATH SETUP
# =========================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# =========================
# IMPORT MODULES
# =========================
from language.translator import translate
from language.voice import speak_alert
from driver_monitoring.drowsiness import detect_drowsiness
from driver_monitoring.distraction import detect_distraction

from vehicle_health.predict import predict_vehicle_health
from vehicle_health.fault_detection import detect_fault
from vehicle_health.rul_prediction import predict_rul

from risk_engine.risk_assessment import calculate_risk

from recommendation_engine.recommendation import (
    generate_recommendation
)

from maintenance.maintenance_scheduler import (
    generate_maintenance_schedule
)

# =========================
# STREAMLIT CONFIG
# =========================
st.markdown("""
<style>

/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Selected value */
div[data-baseweb="select"] * {
    color: black !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    color: black !important;
    background-color: white !important;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="A V C",
    layout="wide"
)

st.markdown("""
<style>

/* Matte Black Background */
.stApp {
    background: linear-gradient(
        135deg,
        #050505 0%,
        #111111 50%,
        #1a1a1a 100%
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #333333;
}

/* Sidebar title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* FIX SLIDER LABELS */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #ffffff !important;
    font-weight: 600;
}

/* Slider values */
.stSlider label {
    color: #ffffff !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Headers */
h1, h2, h3 {
    color: #ffffff !important;
}

/* Info Cards */
.stAlert {
    border-radius: 12px;
}

/* Remove Streamlit top bar */
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)
# =========================
# PROFESSIONAL DARK THEME
# =========================

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: radial-gradient(
        circle at top,
        #1a1a1a 0%,
        #0d0d0d 30%,
        #000000 100%
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b0b0b;
    border-right: 1px solid #222222;
}

/* Headers */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* Info Cards */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    border-radius: 12px;
    border: none;
}

/* Progress Bars */
.stProgress > div > div > div > div {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
}

/* Camera Frame */
img {
    border-radius: 20px;
    border: 2px solid #374151;
}

/* Cards Effect */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111827;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4b5563;
}

/* Section Containers */
div[data-testid="stVerticalBlock"] > div {
    border-radius: 15px;
}

/* Metrics Text */
[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

/* Recommendation Boxes */
.element-container .stInfo {
    border-radius: 12px;
}

/* Smooth Animations */
* {
    transition: all 0.3s ease;
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>

/* Sidebar selectbox */
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: black !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: white !important;
}

</style>
""", unsafe_allow_html=True)


if "last_voice_alert" not in st.session_state:

    st.session_state.last_voice_alert = ""

if "last_voice_time" not in st.session_state:

    st.session_state.last_voice_time = 0

CRITICAL_COOLDOWN = 5
WARNING_COOLDOWN = 10
NORMAL_COOLDOWN = 15

# =========================
# HEADER
# =========================


# =========================
# LANGUAGE SELECTION
# =========================

language_map = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de"
}

selected_language = st.sidebar.selectbox(
    "Language",
    list(language_map.keys()), index = 0
)

lang = language_map[selected_language]



st.markdown(f"""
<h1 style='
text-align:center;
font-size:48px;
color:white;
letter-spacing:3px;
'> {translate("title", lang)}
</h1>

<p style='
text-align:center;
color:#aaaaaa;
font-size:18px;
'>
 ___________________________________________________
</p>
""", unsafe_allow_html=True)


# =========================
# SYSTEM OVERVIEW
# =========================

st.markdown("---")
# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.markdown(
    f"<h2 style='color:black;'>{translate('vehicle_inputs', lang)}</h2>",
    unsafe_allow_html=True
)

engine_temp = st.sidebar.slider(
    translate("engine_temperature", lang),
    50,
    150,
    90
)

battery_voltage = st.sidebar.slider(
    translate("battery_voltage", lang),
    8.0,
    15.0,
    12.5
)

rpm = st.sidebar.slider(
    translate("engine_rpm", lang),
    500,
    8000,
    2500
)

fuel_efficiency = st.sidebar.slider(
    translate("fuel_efficiency", lang),
    5.0,
    30.0,
    15.0
)
fuel_level = st.sidebar.slider(
    translate("fuel_level", lang),
    0,
    100,
    50
)

# =========================
# CAMERA INITIALIZATION
# =========================

if "camera" not in st.session_state:

    st.session_state.camera = cv2.VideoCapture(0)

cap = st.session_state.camera

# =========================
# MAIN PROCESS
# =========================

try:

    success, frame = cap.read()

    if not success:

        st.error(
            translate("webcam_error", lang)
)

        st.stop()

    # =========================
    # LIVE CAMERA
    # =========================

    st.image(
        frame,
        channels="BGR",
        use_container_width = True
    )

    # =========================
    # DRIVER MONITORING
    # =========================

    drowsiness_result = detect_drowsiness(
        frame
    )

    distraction_result = detect_distraction(
        frame
    )

    # =========================
    # VEHICLE HEALTH
    # =========================

    vehicle_result = predict_vehicle_health(
        engine_temp,
        battery_voltage,
        rpm,
        fuel_efficiency
    )

    # =========================
    # FAULT DETECTION
    # =========================

    fault_result = detect_fault(
        engine_temp,
        battery_voltage,
        rpm,
        fuel_efficiency
    )

    # =========================
    # RUL PREDICTION
    # =========================

    rul_result = predict_rul(
        vehicle_result["health_score"],
        engine_temp,
        battery_voltage,
        rpm
    )

    # =========================
    # RISK ASSESSMENT
    # =========================

    risk_result = calculate_risk(

        drowsiness_result["status"],

        distraction_result["status"],

        vehicle_result["status"],

        fault_result["severity"],

        vehicle_result["health_score"],

        rul_result["battery_life_months"],

        rul_result["service_due_km"]

    )

    # =========================
    # MAINTENANCE SCHEDULER
    # =========================

    maintenance_result = (
        generate_maintenance_schedule(

            fault_result["fault_type"],

            vehicle_result["status"],

            rul_result["battery_life_months"],

            rul_result["service_due_km"]

        )
    )

    # =========================
    # RECOMMENDATIONS
    # =========================

    recommendations = generate_recommendation(

        drowsiness_result["status"],

        distraction_result["status"],

        translate(
        vehicle_result["status"].lower(), lang
        ),

        translate(
        risk_result["risk_level"].lower().replace(" ", "_"),
        lang
        ),

        fault_result["fault_type"],

        rul_result["battery_life_months"],

        rul_result["service_due_km"],

        fuel_level=fuel_level

    )

    voice_message = None
    cooldown = NORMAL_COOLDOWN

    # Critical Risk

    if risk_result["risk_level"] == "Critical":

        voice_message = translate(
            "voice_critical", lang
        )
        cooldown = CRITICAL_COOLDOWN

    # Driver Drowsiness

    elif drowsiness_result["status"] == "Drowsy":

        voice_message = translate(
            "voice_drowsy", lang
        )
        cooldown = WARNING_COOLDOWN

    # Phone Usage

    elif distraction_result["status"] == "Distracted":

        voice_message = translate(
            "voice_phone", lang
        )
        cooldown = WARNING_COOLDOWN

    # Engine Fault

    elif fault_result["fault_type"] == "engine_overheating":

        voice_message = translate(
            "voice_engine_hot", lang
        )
        cooldown = WARNING_COOLDOWN

    # Battery Warning

    elif rul_result["battery_life_months"] <= 5:

        voice_message = translate(
            "voice_battery_low", lang
        )
        cooldown = WARNING_COOLDOWN


    # Fuel Warning

    elif fuel_level <= 15:

        voice_message = translate(
            "voice_fuel_low", lang
    )

    cooldown = WARNING_COOLDOWN

    # Cooldown Logic

    current_time = time.time()

    if voice_message:

        elapsed_time = (
            current_time
            - st.session_state.last_voice_time
        )

        if (
            voice_message
            != st.session_state.last_voice_alert
        ) or (
            elapsed_time
            >= cooldown
        ):
            print("Voice Alert", voice_message)
            speak_alert(
                voice_message,
                lang
            )
            
            

            st.session_state.last_voice_alert = (
                voice_message
            )

            st.session_state.last_voice_time = (
                current_time
            )

        st.subheader(
            translate("ai_voice_assistant", lang)
        )
        st.info(
            voice_message
        )
    # =========================
    # DRIVER MONITORING UI
    # =========================

    st.subheader(
        f"{translate('driver_monitoring', lang)}"
    )
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
    translate("driver_status", lang),
    translate(drowsiness_result["status"].lower(), lang)
)

    with col2:
        st.metric(
            "EAR",
            drowsiness_result["ear"]
        )

    with col3:
        st.metric(
            translate("closed_frames", lang),
            drowsiness_result["closed_frames"]
        )

    with col4:
        st.metric(
            translate("phone_detected", lang),
            str(distraction_result["phone_detected"])
        )
    st.metric(
        translate("phone_confidence", lang),
        distraction_result[
            "confidence"
        ]
    )

    # =========================
    # VEHICLE HEALTH UI
    # =========================

    st.subheader(
        f"{translate('vehicle_health', lang)}"
    )

    col5, col6, col7 = st.columns(3)

    with col5:

        vehicle_status = vehicle_result["status"].strip().lower()
        
        st.metric(
            translate("vehicle_status", lang),
            translate(vehicle_status, lang)
    )
    with col6:

        st.metric(
    translate("prediction_confidence", lang),
    round(vehicle_result["probability"], 2)
)

    with col7:

        st.metric(
            translate("health_score", lang),
            f"{vehicle_result['health_score']}%"
        )

    st.progress(
        vehicle_result["health_score"] / 100
    )

    if vehicle_result["health_score"] >= 80:

        st.success(
    translate("vehicle_health_excellent", lang)
)

    elif vehicle_result["health_score"] >= 60:

        st.warning(
            translate("vehicle_health_moderate", lang)
        )

    else:

        st.error(
            translate("vehicle_health_poor", lang)
        )

    # =========================
    # FAULT DETECTION UI
    # =========================

    st.subheader(
        f"{translate('fault_detection', lang)}"
    )

    col8, col9 = st.columns(2)

    with col8:

        st.metric(
            translate("fault_type", lang),
            translate(fault_result["fault_type"], lang)
        )

    with col9:
        st.metric(
            translate("fault_severity", lang),
            translate(fault_result["severity"].lower(), lang)
        )

    if fault_result["severity"] == "High":

        st.error(
            translate("high_severity_fault", lang)
        )

    elif fault_result["severity"] == "Medium":

        st.warning(
            translate("medium_severity_fault", lang)
        )

    else:

        st.success(
            translate("vehicle_operating_normally", lang)
        )
         # =========================
    # RUL UI
    # =========================

    st.subheader(
    translate("predictive_maintenance", lang)
)

    col10, col11, col12, col13 = st.columns(4)

    with col10:

        st.metric(
            translate("battery_life", lang),
            f"{rul_result['battery_life_months']} {translate('months', lang)}"
        )

    with col11:

        st.metric(
            translate("service_due", lang),
            f"{rul_result['service_due_km']} {translate('km', lang)}"

        )

    with col12:

        rul_status = rul_result.get("status", "Unknown")

        st.metric(
            translate("rul_status", lang),
            translate(rul_status.lower(), lang)
        )
    battery_percentage = min(
        100,
        int(
            rul_result["battery_life_months"] * 100 / 12
        )
    )
    with col13:

        st.metric(
            translate("fuel_level", lang),
            f"{fuel_level}%"
)

    st.progress(
        battery_percentage / 100
    )
    st.subheader(
        translate("fuel_level", lang)
    )
    st.progress(fuel_level / 100)
    

    if fuel_level <= 15:

        st.warning(
            translate("fuel_low", lang)
    )   

    elif fuel_level <= 30:

        st.info(
            translate("fuel_getting_low", lang)
)
    # =========================
    # RISK UI
    # =========================

    st.subheader(
        f"{translate('risk_assessment', lang)}"
    )

    col13, col14 = st.columns(2)

    with col13:

        st.metric(
            translate("safety_score", lang),
            risk_result["safety_score"]
        )

    with col14:

        st.metric(
    translate("risk_level", lang),
    translate(risk_result["risk_level"].lower(), lang)
)

    # =========================
    # MAINTENANCE UI
    # =========================

    st.subheader(
    translate("predictive_maintenance", lang)
)


    for item in maintenance_result:
        st.success(
            translate(item, lang)
        )
    # =========================
    # RECOMMENDATIONS UI
    # =========================

    st.subheader(
        f"{translate('recommendations', lang)}"
    )

    for recommendation in recommendations:
        st.info(
            translate(recommendation, lang)
        )

    # =========================
    # ALERT BANNER
    # =========================

    # =========================
# ALERT BANNER
# =========================

    if risk_result["risk_level"] == "Critical":

        st.error(
            translate("critical_risk", lang)
        )

    elif risk_result["risk_level"] == "High":

        st.warning(
            translate("high_risk", lang)
        )

    elif risk_result["risk_level"] == "Medium":

        st.info(
            translate("medium_risk", lang)
        )

    else:

        st.success(
            translate("low_risk", lang)
        )
    # =========================
    # PROJECT SUMMARY
    # =========================

    st.markdown("---")

    st.subheader(
        f"{translate('summary', lang)}"
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            translate("vehicle_health", lang),
            f"{vehicle_result['health_score']}%"
)

    with summary_col2:

        st.metric(
            translate("safety_score", lang),
            risk_result["safety_score"]
)

    with summary_col3:

        st.metric(
            translate("fault_severity", lang),
            translate(fault_result["severity"].lower(), lang)
)

    # =========================
    # AUTO REFRESH
    # =========================

    time.sleep(
        1
    )
    st.empty()
    st.rerun()

except Exception as e: 

    st.error(
        f"{translate('application_error', lang)}: {e}"
    )

    st.exception(
        e
    )