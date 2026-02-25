import streamlit as st
import pandas as pd

st.title("Insights")

if "fis_result" not in st.session_state:
    st.warning("No FIS report found. Go to Home to initialize.")
    st.stop()

report = st.session_state["fis_result"]["fis_report"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Income Insights")
    st.json(report["income_insights"])

    st.subheader("Trend Insights")
    st.json(report["trend_insights"])

with col2:
    st.subheader("Habits")
    st.json(report["habits"])

    st.subheader("Discipline Risk")
    st.json(report["discipline_risk"])

st.subheader("Forecast")
st.json(report["forecast"])