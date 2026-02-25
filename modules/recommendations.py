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
    persona = report.get("persona_profile", {})  # NEW: persona-aware recs

    # =====================================================
    # CORE FINANCIAL HEALTH
    # =====================================================
    if fh < 40:
        recs.append("Your financial health is weak — prioritize reducing debt and increasing savings immediately.")
    elif fh < 60:
        recs.append("Strengthen your core financial health by improving savings rate and reducing high-interest debt.")

    # =====================================================
    # EMERGENCY FUND
    # =====================================================
    if emergency.get("months_covered", 0) < 1:
        recs.append("Your emergency fund is critically low — aim to save at least one month of expenses as soon as possible.")
    elif emergency.get("months_covered", 0) < 3:
        recs.append("Increase your emergency fund contributions until you reach at least 3 months of expenses.")

    # =====================================================
    # DISCIPLINE RISK
    # =====================================================
    if discipline in ("High", "Critical"):
        recs.append("Your discipline risk is elevated — review your budget and reduce discretionary spending.")

    # =====================================================
    # INCOME INSIGHTS
    # =====================================================
    if income.get("income_health") in ("Volatile", "Declining"):
        recs.append("Your income is unstable — consider building a larger cash buffer or diversifying income sources.")

    # Persona-specific income advice
    if persona.get("type") == "freelancer":
        recs.append("As a freelancer, set aside 25–30% of income for taxes and prepare for seasonal fluctuations.")
    elif persona.get("type") == "commission_sales":
        recs.append("Your income is commission-based — maintain a larger emergency buffer to smooth out slow months.")
    elif persona.get("type") == "student":
        recs.append("As a student, prioritize low-cost budgeting and avoid high-interest debt.")

    # =====================================================
    # EXPENSE & SAVINGS TRENDS
    # =====================================================
    expense_trend = trends.get("expense_trend", {})
    if expense_trend.get("health") == "Worsening":
        recs.append("Your expenses are trending up — identify categories to cut back on this month.")

    savings_trend = trends.get("savings_trend", {})
    if savings_trend.get("health") in ("Weakening", "Volatile"):
        recs.append("Your savings trend is weakening — commit to a fixed monthly savings amount and automate it.")

    # =====================================================
    # HABITS
    # =====================================================
    habit_score = habits["consistency"]["score"]
    if habit_score < 40:
        recs.append("Your financial habits are inconsistent — set a weekly check-in to log and review spending.")
    elif habit_score < 60:
        recs.append("Improving your financial consistency will help stabilize your long-term progress.")

    # =====================================================
    # GOALS
    # =====================================================
    for name, g in goals.items():
        rec_text = g["recommendation"]["recommendation"]
        if "Increase monthly savings" in rec_text:
            recs.append(f"For goal '{name}': {rec_text}")
        elif "ahead of schedule" in rec_text.lower():
            recs.append(f"Great job on '{name}' — you're ahead of schedule. Maintain your current pace.")

    # =====================================================
    # FORECAST
    # =====================================================
    if forecast.get("confidence", 0) < 0.4:
        recs.append("Your expense forecast is highly volatile — focus on stabilizing spending patterns.")

    # =====================================================
    # OVERALL FIS
    # =====================================================
    if fis < 60:
        recs.append("Your overall Financial Intelligence Score suggests room for improvement — focus on one area at a time.")

    # =====================================================
    # DEDUPLICATE
    # =====================================================
    seen = set()
    unique_recs = []
    for r in recs:
        if r not in seen:
            seen.add(r)
            unique_recs.append(r)

    return unique_recs