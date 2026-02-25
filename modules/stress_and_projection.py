from typing import Dict, Any
from .financial_health import (
    cashflow_score, emergency_score, debt_health_score,
    investing_readiness_score, financial_health_score
)
from .discipline_risk import calculate_discipline_risk


def financial_intelligence_score(
    snapshot,
    income_insights: Dict[str, Any],
    trend_insights: Dict[str, Any],
    habits: Dict[str, Any],
    forecast: Dict[str, Any],
    goal_insights: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes an advanced Financial Intelligence Score (FIS v2).

    Combines:
    - Financial Health (cashflow, savings, emergency, debt, investing)
    - Discipline Risk
    - Income Health & Reliability
    - Expense & Savings Trend Health
    - Habit Consistency & Momentum
    - Forecast Confidence
    - Goal Progress & Goal Forecasting
    """

    # =====================================================
    # 1️⃣ Financial Health Subscores
    # =====================================================
    cashflow = cashflow_score(snapshot.savings_rate)
    emergency = emergency_score(snapshot.emergency_months)
    debt = debt_health_score(snapshot.has_high_interest_debt, snapshot.liquid_assets_to_debt)
    investing = investing_readiness_score(snapshot.investments > 0, snapshot.emergency_months)

    fin_health = financial_health_score(
        cashflow, cashflow, emergency, debt, investing
    )
    fin_health_score = fin_health["score"]  # 0–100


    # =====================================================
    # 2️⃣ Discipline Risk
    # =====================================================
    risk = calculate_discipline_risk(entries=[], budget_comparison=None)
    risk_factor = {
        "Low": 1.0,
        "Moderate": 0.9,
        "High": 0.75,
        "Critical": 0.5
    }.get(risk["risk_level"], 0.9)


    # =====================================================
    # 3️⃣ Income Intelligence
    # =====================================================
    income_health = income_insights["income_health"]
    reliability = income_insights["reliability_score"]  # 0–100

    income_factor = 1.0
    if income_health == "Strong & Growing":
        income_factor = 1.05
    elif income_health == "Stable":
        income_factor = 1.0
    elif income_health == "Volatile":
        income_factor = 0.9
    elif income_health == "Declining":
        income_factor = 0.8


    # =====================================================
    # 4️⃣ Expense & Savings Trend Intelligence
    # =====================================================
    expense_health = trend_insights["expense_trend"]["health"]
    savings_health = trend_insights["savings_trend"]["health"]

    trend_factor = 1.0

    if expense_health == "Worsening":
        trend_factor -= 0.05
    elif expense_health == "Improving":
        trend_factor += 0.03

    if savings_health == "Strong":
        trend_factor += 0.05
    elif savings_health == "Weakening":
        trend_factor -= 0.05

    trend_factor = max(0.8, min(1.1, trend_factor))


    # =====================================================
    # 5️⃣ Habit Intelligence
    # =====================================================
    habit_score = habits["consistency"]["score"]  # 0–100
    momentum = habits["momentum"]

    habit_factor = 1.0
    if habit_score >= 70:
        habit_factor += 0.05
    elif habit_score < 40:
        habit_factor -= 0.05

    if momentum == "Improving":
        habit_factor += 0.03
    elif momentum == "Declining":
        habit_factor -= 0.03

    habit_factor = max(0.85, min(1.1, habit_factor))


    # =====================================================
    # 6️⃣ Forecast Confidence
    # =====================================================
    forecast_conf = forecast["confidence"]  # 0–1

    forecast_factor = 0.9 + (forecast_conf * 0.2)  # 0.9–1.1


    # =====================================================
    # 7️⃣ Goal Intelligence
    # =====================================================
    goal_factor = 1.0
    for g in goal_insights.values():
        rec = g["recommendation"]["recommendation"]
        if "Increase monthly savings" in rec:
            goal_factor -= 0.03
        elif "on track" in rec.lower():
            goal_factor += 0.02

    goal_factor = max(0.85, min(1.1, goal_factor))


    # =====================================================
    # 8️⃣ Composite FIS v2
    # =====================================================
    composite = (
        fin_health_score *
        risk_factor *
        income_factor *
        trend_factor *
        habit_factor *
        forecast_factor *
        goal_factor
    )

    composite_score = round(max(1, min(100, composite)))


    # Classification
    if composite_score >= 80:
        status = "Excellent"
    elif composite_score >= 60:
        status = "Good"
    elif composite_score >= 40:
        status = "Fair"
    else:
        status = "Poor"


    return {
        "score": composite_score,
        "status": status,
        "financial_health_score": fin_health_score,
        "discipline_risk_level": risk["risk_level"],
        "income_factor": round(income_factor, 3),
        "trend_factor": round(trend_factor, 3),
        "habit_factor": round(habit_factor, 3),
        "forecast_factor": round(forecast_factor, 3),
        "goal_factor": round(goal_factor, 3)
    }