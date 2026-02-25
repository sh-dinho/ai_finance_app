import streamlit as st

st.title("🎯 Goals & Forecasting")

if "fis_result" not in st.session_state:
    st.warning("Please initialize data on the Home page.")
    st.stop()

report = st.session_state["fis_result"]["fis_report"]
goal_progress = report["goals"]
goal_insights = report["goal_insights"]

for name, progress in goal_progress.items():
    with st.container(border=True):
        c1, c2 = st.columns([1, 2])

        with c1:
            st.markdown(f"### {name}")
            st.metric("Progress", f"{int(progress['progress'] * 100)}%")
            st.caption(f"Status: {progress['status']}")

        with c2:
            insight = goal_insights[name]
            st.progress(progress['progress'])
            st.write(f"📅 **Projected Completion:** {insight['forecast']['projected_completion_date']}")

            if insight['forecast']['will_meet_deadline']:
                st.write("✅ On track for your target date.")
            else:
                st.error(f"⚠️ {insight['recommendation']['recommendation']}")