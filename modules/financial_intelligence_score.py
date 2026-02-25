from typing import Dict, Any
import logging
from .financial_health import (
    cashflow_score, emergency_score, debt_health_score,
    investing_readiness_score, financial_health_score
)
from .discipline_risk import calculate_discipline_risk

logger = logging.getLogger(__name__)


def financial_intelligence_score(
        snapshot: Any,
        income_insights: Dict[str, Any],
        trend_insights: Dict[str, Any],
        habits: Dict[str, Any],
        forecast: Dict[str, Any],
        goal_insights: Dict[str, Any],
        df_daily: Any
) -> Dict[str, Any]:
    """
    FIS v2: Fixed shadowing bugs and improved factor weighting.
    """
    # 1. Financial Health Subscores
    cf_score = cashflow_score(snapshot.savings_rate)
    em_score = emergency_score(snapshot.emergency_months)
    db_score = debt_health_score(snapshot.has_high_interest_debt, snapshot.liquid_assets_to_debt)
    inv_score = investing_readiness_score(snapshot.is_investing, snapshot.emergency_months)

    # FIXED: Using distinct variables for health components
    health_result = financial_health_score(
        cashflow=cf_score,
        savings=cf_score,  # Can be expanded to a separate metric later
        emergency=em_score,
        debt=db_score,
        investing=inv_score
    )
    fin_health_score = health_result["score"]

    # 2. Factor Calculation (Normalization)
    # Income Factor: Reliability score / 100
    income_factor = max(0.7, income_insights.get("reliability_score", 50) / 100)

    # Trend Factor: Penalize if expenses > income trend
    trend_factor = 1.05 if snapshot.income_trend > snapshot.expense_trend else 0.90

    # Habit Factor: Consistency status mapping
    habit_map = {"Excellent": 1.1, "Moderate": 1.0, "Weak": 0.8}
    habit_factor = habit_map.get(habits.get("status"), 0.9)

    # 3. Composite Calculation
    # Base score weighted by external behaviors
    raw_score = fin_health_score * income_factor * trend_factor * habit_factor
    final_score = round(max(1, min(100, raw_score)))

    return {
        "score": final_score,
        "status": _get_status(final_score),
        "financial_health_score": fin_health_score,
        "income_factor": income_factor,
        "trend_factor": trend_factor,
        "habit_factor": habit_factor
    }


def _get_status(score: int) -> str:
    if score >= 80: return "Excellent"
    if score >= 60: return "Good"
    if score >= 40: return "Fair"
    return "Poor"