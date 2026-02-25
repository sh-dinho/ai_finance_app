# modules/recommendations.py
from typing import Dict, Any, List


def generate_recommendations(report: Dict[str, Any]) -> List[str]:
    recs: List[str] = []

    fh = report["intelligence_score"]["financial_health_score"]
    fis = report["intelligence_score"]["score"]
    discipline = report["discipline_risk"]["risk_level"]
    emergency = report["emergency_fund"]
    income = report["income_insights"]
    trends = report.get("trend_insights", {})
    habits = report["habits"]
    goals = report["goal_insights"]
    forecast = report["forecast"]

    # Financial health
    if fh < 60:
        recs.append("Strengthen your core financial health by improving savings rate and reducing high-interest debt.")

    # Emergency fund
    if emergency.get("months_covered", 0) < 3:
        recs.append("Increase your emergency fund contributions until you reach at least 3 months of expenses.")

    # Discipline risk
    if discipline in ("High", "Critical"):
        recs.append("Your discipline risk is elevated—review your budget and reduce discretionary spending.")

    # Income
    if income.get("income_health") in ("Volatile", "Declining"):
        recs.append("Your income is unstable—consider building a larger cash buffer or diversifying income sources.")

    # Expense trend
    expense_trend = trends.get("expense_trend", {})
    if expense_trend.get("health") == "Worsening":
        recs.append("Your expenses are trending up—identify categories to cut back on this month.")

    # Savings trend
    savings_trend = trends.get("savings_trend", {})
    if savings_trend.get("health") in ("Weakening", "Volatile"):
        recs.append("Your savings trend is weakening—commit to a fixed monthly savings amount and automate it.")

    # Habits
    habit_score = habits["consistency"]["score"]
    if habit_score < 40:
        recs.append("Your financial habits are inconsistent—set a recurring weekly check-in to log and review spending.")

    # Goals
    for name, g in goals.items():
        rec_text = g["recommendation"]["recommendation"]
        if "Increase monthly savings" in rec_text:
            recs.append(f"For goal '{name}': {rec_text}")

    # Forecast
    if forecast.get("confidence", 0) < 0.4:
        recs.append("Your expense forecast is highly volatile—focus on stabilizing spending patterns.")

    # Overall FIS
    if fis < 60:
        recs.append("Your overall Financial Intelligence Score suggests room for improvement—focus on one area at a time.")

    # Deduplicate while preserving order
    seen = set()
    unique_recs = []
    for r in recs:
        if r not in seen:
            seen.add(r)
            unique_recs.append(r)

    return unique_recs