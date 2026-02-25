import streamlit as st

st.title("Goals & Forecasting")

if "fis_result" not in st.session_state:
    st.warning("No FIS report found. Go to Home to initialize.")
    st.stop()

report = st.session_state["fis_result"]["fis_report"]
goal_progress = report["goals"]
goal_insights = report["goal_insights"]

st.subheader("Goal Progress")
for name, g in goal_progress.items():
    st.write(f"### {name}")
    st.progress(g["progress"])
    cols = st.columns(3)
    cols[0].metric("Current", g["current_value"])
    cols[1].metric("Target", g["target"])
    cols[2].metric("Status", g["status"])

st.subheader("Goal Forecast & Recommendations")
for name, g in goal_insights.items():
    st.write(f"#### {name}")
    forecast = g["forecast"]
    rec = g["recommendation"]
    st.write(f"- Projected completion: **{forecast['projected_completion_date']}**")
    st.write(f"- Will meet deadline: **{forecast['will_meet_deadline']}**")
    st.write(f"- Recommendation: {rec['recommendation']}")