import streamlit as st
import pandas as pd

from modules.report_card import build_financial_report_card, summarize_financial_life
from modules.financial_intelligence import financial_intelligence_score

# You’ll need to wire in your own data pipeline here
from mock_data.generator import generate_mock_persona
from modules.core import calculate_basic_metrics
from modules.income_insights import income_summary
from modules.discipline_risk import calculate_discipline_risk
from modules.goals import evaluate_goals, generate_goal_insights


def main():
    st.title("Financial Intelligence Dashboard")

    persona = st.selectbox(
        "Choose persona",
        [
            "freelancer",
            "stable_salaried",
            "high_earner_spender",
            "financially_stressed",
            "young_investor",
            "near_retirement",
            "student",
            "family_childcare",
            "commission_sales",
            "seasonal_worker",
        ],
    )

    months = st.slider("Months of history", 6, 36, 24)

    if st.button("Run Analysis"):
        data = generate_mock_persona(persona, months=months)

        snapshot = data["snapshot"]
        entries = data["entries"]
        df_daily = data["df_daily"]
        goals = data["goals"]
        current_goal_values = data["current_goal_values"]

        metrics = calculate_basic_metrics(snapshot)
        income = income_summary(entries)
        discipline = calculate_discipline_risk(df_daily)
        goal_progress = evaluate_goals(goals, current_goal_values, snapshot)
        goal_insights = generate_goal_insights(goals, goal_progress, metrics["savings"])

        # You’ll need to compute trend_insights and forecast in your pipeline
        trend_insights = {}  # placeholder
        forecast = {"confidence": 0.5}  # placeholder
        persona_profile = {"type": persona}

        fis = financial_intelligence_score(
            snapshot,
            income_insights=income,
            trend_insights=trend_insights,
            habits={"consistency": {"score": 60}, "momentum": "Stable"},
            forecast=forecast,
            goal_insights=goal_insights,
            df_daily=df_daily,
            persona_profile=persona_profile,
        )

        report_card = build_financial_report_card(fis)
        summary = summarize_financial_life(
            fis, discipline, income, {"months_covered": snapshot.emergency_months}, goal_progress
        )

        st.subheader("Overall Score")
        st.metric("FIS Score", report_card["score"], report_card["status"])
        st.write(f"Grade: **{report_card['grade']}**")
        st.write(summary)

        st.subheader("Subscores")
        st.dataframe(pd.DataFrame(report_card["subscores"], index=["Score"]).T)

        st.subheader("Discipline Risk")
        st.json(discipline)

        st.subheader("Goal Insights")
        st.json(goal_insights)


if __name__ == "__main__":
    main()