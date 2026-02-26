from scoring.utils import clamp


def financial_intelligence_score(
    snapshot,
    income_insights,
    trend_insights,
    habits,
    forecast,
    goal_insights,
    settings
):
    w = settings.weights.composite.factors

    income_score = income_insights.get("reliability_score", 50)
    trend_score = trend_insights.get("trend_score", 50)
    habit_score = habits.get("score", 50)
    goal_score = goal_insights.get("goal_health_score", 50)

    final_score = (
        income_score * w.income +
        trend_score * w.trend +
        habit_score * w.habits +
        goal_score * w.goals
    )

    status = (
        "Excellent" if final_score >= settings.thresholds.status.excellent
        else "Good" if final_score >= settings.thresholds.status.good
        else "Fair" if final_score >= settings.thresholds.status.fair
        else "Poor"
    )

    return {
        "score": clamp(final_score),
        "status": status,
        "components": {
            "income": income_score,
            "trend": trend_score,
            "habits": habit_score,
            "goals": goal_score,
        }
    }
