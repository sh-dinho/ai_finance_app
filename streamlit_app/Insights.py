import streamlit as st

st.title("🧠 Deep Insights")

if "fis_result" not in st.session_state:
    st.stop()

report = st.session_state["fis_result"]["fis_report"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Income Reliability")
    inc = report["income_insights"]
    st.metric("Reliability Score", inc["reliability_score"])
    st.write(f"Health: **{inc['income_health']}**")
    st.json(inc["trend"])

with col2:
    st.subheader("📉 Discipline & Risk")
    risk = report["discipline_risk"]
    st.error(f"Risk Level: {risk['risk_level']}")
    for factor in risk["risk_factors"]:
        st.write(f"- {factor}")

st.divider()
st.subheader("🔄 Habit Momentum")
st.json(report["habits"])