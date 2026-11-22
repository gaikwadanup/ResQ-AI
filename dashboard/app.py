
import sys
import re
import subprocess
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------- PROJECT SETUP ----------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.weather_api import get_weather


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ResQ AI | Emergency Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 1.5rem;
}

div[data-testid="stMetric"] {
    background-color: #1b2430;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #303b4b;
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.title("🛡️ ResQ AI")

st.subheader(
    "AI-Powered Disaster Monitoring & Coordination System"
)

st.caption(
    "Emergency Operations Dashboard | Sangli, Maharashtra"
)

st.divider()


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Control Panel")

scenario = st.sidebar.selectbox(
    "Select Risk Scenario",
    ["LIVE", "LOW", "MODERATE", "HIGH"]
)

st.sidebar.info(
    "LIVE uses weather data from Open-Meteo. "
    "Other scenarios use simulated demonstration data."
)

run_button = st.sidebar.button(
    "🚀 Run ResQ AI",
    use_container_width=True
)


# ---------------- WEATHER MONITORING ----------------

st.header("🌦️ Live Weather Monitoring")

with st.spinner("Fetching weather information..."):
    weather = get_weather()

if weather:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Temperature",
        f"{weather['temperature']} °C"
    )

    col2.metric(
        "Humidity",
        f"{weather['humidity']} %"
    )

    col3.metric(
        "Current Rainfall",
        f"{weather['rainfall']} mm"
    )

    col4.metric(
        "Wind Speed",
        f"{weather['wind_speed']} km/h"
    )

    st.caption(
        f"Weather data time: {weather['time']} | "
        "Source: Open-Meteo"
    )

else:

    st.warning(
        "Live weather data is currently unavailable."
    )


# ---------------- WEATHER FORECAST CHARTS ----------------

if weather:

    st.divider()

    st.header("📈 24-Hour Weather Forecast")

    forecast_df = pd.DataFrame({
        "Time": pd.to_datetime(weather["hourly_time"]),
        "Rainfall (mm)": weather["hourly_rainfall"],
        "Rain Probability (%)": weather["rain_probability"],
        "Wind Speed (km/h)": weather["hourly_wind"]
    })

    col1, col2 = st.columns(2)

    with col1:

        rainfall_fig = px.bar(
            forecast_df,
            x="Time",
            y="Rainfall (mm)",
            title="Hourly Rainfall Forecast"
        )

        rainfall_fig.update_layout(
            template="plotly_dark",
            height=350,
            xaxis_title="Time",
            yaxis_title="Rainfall (mm)"
        )

        st.plotly_chart(
            rainfall_fig,
            use_container_width=True
        )

    with col2:

        probability_fig = px.line(
            forecast_df,
            x="Time",
            y="Rain Probability (%)",
            title="Hourly Rain Probability",
            markers=True
        )

        probability_fig.update_layout(
            template="plotly_dark",
            height=350,
            xaxis_title="Time",
            yaxis_title="Probability (%)",
            yaxis_range=[0, 100]
        )

        st.plotly_chart(
            probability_fig,
            use_container_width=True
        )

    wind_fig = px.line(
        forecast_df,
        x="Time",
        y="Wind Speed (km/h)",
        title="Hourly Wind Speed",
        markers=True
    )

    wind_fig.update_layout(
        template="plotly_dark",
        height=300,
        xaxis_title="Time",
        yaxis_title="Wind Speed (km/h)"
    )

    st.plotly_chart(
        wind_fig,
        use_container_width=True
    )


st.divider()


# ---------------- AI AGENT COORDINATION ----------------

st.header("🤖 AI Agent Coordination")

st.write(
    "Select a scenario from the sidebar and run the complete "
    "ResQ AI multi-agent workflow."
)

if run_button:

    scenario_number = (
        ["LIVE", "LOW", "MODERATE", "HIGH"].index(scenario) + 1
    )

    with st.spinner("ResQ AI agents are working..."):

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "agents.coordinator"
                ],
                input=f"{scenario_number}\n",
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=300
            )

            st.session_state["agent_output"] = result.stdout

            if result.returncode == 0:

                st.session_state["agent_error"] = ""

            else:

                st.session_state["agent_error"] = (
                    result.stderr or
                    "Coordinator exited with an error."
                )

        except subprocess.TimeoutExpired:

            st.session_state["agent_error"] = (
                "The workflow took too long. Please try again."
            )

            st.session_state["agent_output"] = ""

        except Exception as error:

            st.session_state["agent_error"] = str(error)

            st.session_state["agent_output"] = ""


# ---------------- RESULTS ----------------

if "agent_output" in st.session_state:

    output = st.session_state["agent_output"]

    if st.session_state.get("agent_error"):

        st.error(
            "An error occurred while running the agents."
        )

        st.code(
            st.session_state["agent_error"],
            language="text"
        )

    if output:

        # ---------------- RISK ASSESSMENT ----------------

        st.subheader("📊 Risk Assessment")

        risk_match = re.search(
            r"Risk Level:\s*(LOW|MODERATE|HIGH)",
            output
        )

        score_match = re.search(
            r"Risk Score:\s*(\d+)",
            output
        )

        decision_match = re.search(
            r"Decision:\s*(MONITOR|PREPARE|MOBILIZE)",
            output
        )

        priority_match = re.search(
            r"Priority:\s*(LOW|MODERATE|HIGH)",
            output
        )

        risk_level = (
            risk_match.group(1)
            if risk_match else "N/A"
        )

        risk_score = (
            score_match.group(1)
            if score_match else "N/A"
        )

        decision = (
            decision_match.group(1)
            if decision_match else "N/A"
        )

        priority = (
            priority_match.group(1)
            if priority_match else "N/A"
        )

        # ---------------- METRICS ----------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Risk Level",
                risk_level
            )

            st.metric(
                "AI Decision",
                decision
            )

        with col2:

            st.metric(
                "Risk Score",
                risk_score
            )

            st.metric(
                "Priority",
                priority
            )

        # ---------------- RISK GAUGE ----------------

        st.divider()

        st.subheader("🎯 Disaster Risk Gauge")

        if risk_score != "N/A":

            gauge_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=float(risk_score),
                    title={
                        "text": "Risk Score (0–10)"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 10],
                            "tickwidth": 1
                        },
                        "bar": {
                            "color": "#38bdf8"
                        },
                        "steps": [
                            {
                                "range": [0, 3],
                                "color": "#14532d"
                            },
                            {
                                "range": [3, 7],
                                "color": "#854d0e"
                            },
                            {
                                "range": [7, 10],
                                "color": "#991b1b"
                            }
                        ],
                        "threshold": {
                            "line": {
                                "color": "white",
                                "width": 4
                            },
                            "thickness": 0.8,
                            "value": float(risk_score)
                        }
                    }
                )
            )

            gauge_fig.update_layout(
                template="plotly_dark",
                height=300,
                margin=dict(
                    t=60,
                    b=20,
                    l=30,
                    r=30
                )
            )

            st.plotly_chart(
                gauge_fig,
                use_container_width=True
            )

        else:

            st.warning(
                "Risk score could not be extracted from agent output."
            )

        # ---------------- RISK STATUS ----------------

        if risk_level == "HIGH":

            st.error("🚨 HIGH RISK DETECTED")

        elif risk_level == "MODERATE":

            st.warning("⚠️ MODERATE RISK DETECTED")

        elif risk_level == "LOW":

            st.success("✅ LOW RISK")

        st.divider()

        # ---------------- AGENT EXECUTION LOGS ----------------

        st.subheader("🧠 Agent Execution Details")

        with st.expander(
            "View complete agent execution logs",
            expanded=True
        ):

            st.text_area(
                "Agent Execution Output",
                value=output,
                height=550,
                disabled=True
            )

        # ---------------- RESOURCE STATUS ----------------

        if "Resources Dispatched: False" in output:

            st.info(
                "No resources were actually dispatched. "
                "The system generated recommendations "
                "for human review."
            )

    elif not st.session_state.get("agent_error"):

        st.warning(
            "No output was returned by the agents."
        )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ResQ AI | AI for Disaster Monitoring and Emergency Coordination | "
    "Prototype Demonstration"
)
