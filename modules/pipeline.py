import logging
from typing import Dict, Any
from .models import FinancialDataBundle, FISReport
from .validation import validate_bundle
from .income_insights import income_summary
from .trend_insights import trend_summary
from .forecasting import forecast_expenses
from .habits import calculate_consistency_metrics
from .goals import analyze_goals
from .financial_intelligence_score import financial_intelligence_score

logger = logging.getLogger(__name__)


def run_fis_pipeline(bundle: FinancialDataBundle) -> Dict[str, Any]:
    """Executes all modules in sequence and generates the final FIS."""

    # 1. Validation
    validate_bundle(bundle)

    # 2. Sequential Analysis
    inc_insights = income_summary(bundle.entries)
    trnd_insights = trend_summary(bundle.entries)
    expense_fc = forecast_expenses(bundle.df_daily)
    habit_metrics = calculate_consistency_metrics(bundle.df_daily, bundle.entries)
    goal_metrics = analyze_goals(bundle.goals, bundle.current_goal_values, bundle.monthly_savings)

    # 3. Final Intelligence Scoring
    intelligence = financial_intelligence_score(
        snapshot=bundle.snapshot,
        income_insights=inc_insights,
        trend_insights=trnd_insights,
        habits=habit_metrics,
        forecast=expense_fc,
        goal_insights=goal_metrics,
        df_daily=bundle.df_daily
    )

    return {
        "intelligence_report": intelligence,
        "insights": {
            "income": inc_insights,
            "trends": trnd_insights,
            "goals": goal_metrics,
            "habits": habit_metrics
        }
    }