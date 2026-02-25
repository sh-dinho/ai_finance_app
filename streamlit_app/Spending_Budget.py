import streamlit as st

st.title("Spending & Budget")

if "fis_result" not in st.session_state:
    st.warning("No FIS report found. Go to Home to initialize.")
    st.stop()

report = st.session_state["fis_result"]["fis_report"]
forecast = report["forecast"]
trend = report["trend_insights"]

st.subheader("Expense Trend")
st.json(trend["expense_trend"])

st.subheader("Savings Trend")
st.json(trend["savings_trend"])

st.subheader("Expense Forecast")
st.json(forecast)