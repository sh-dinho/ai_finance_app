import logging
from typing import Dict, Any

from core.models import FinancialDataBundle
from forecasting.forecasting import forecast_expenses
from income_insights.income_insights import income_summary
from pipeline.errors import MissingDataError
from pipeline.fis_report import FISReport
from scoring.composite import financial_intelligence_score
from scoring.goals import analyze_goals
from scoring.habits import calculate_consistency_metrics
from trend_insights.trend_insights import trend_summary

logger = logging.getLogger("FISPipeline")


class FISPipeline:
    """
    The orchestrator that coordinates all scoring engines, insights,
    forecasting, and configuration-driven behavior.
    """

    def __init__(self, settings):
        self.settings = settings

    def run(self, bundle: FinancialDataBundle) -> FISReport:
        if not bundle:
            raise MissingDataError("FinancialDataBundle is required.")

        logger.info("Starting Financial Intelligence Pipeline")

        insights: Dict[str, Any] = {}

        # Income insights
        if self.settings.features.enable_income_reliability:
            insights["income"] = income_summary(bundle.entries)
        else:
            insights["income"] = {"enabled": False}

        # Trend insights
        if self.settings.features.enable_trend_factor:
            insights["trends"] = trend_summary(bundle.entries)
        else:
            insights["trends"] = {"enabled": False}

        # Forecasting
        if self.settings.features.enable_forecasting:
            insights["forecast"] = forecast_expenses(bundle.df_daily)
        else:
            insights["forecast"] = {"enabled": False}

        # Habits
        if self.settings.features.enable_habit_scoring:
            insights["habits"] = calculate_consistency_metrics(
                bundle.df_daily, bundle.entries
            )
        else:
            insights["habits"] = {"enabled": False}

        # Goals
        if self.settings.features.enable_goal_scoring:
            insights["goals"] = analyze_goals(
                bundle.goals,
                bundle.current_goal_values,
                bundle.monthly_savings
            )
        else:
            insights["goals"] = {"enabled": False}

        # Composite intelligence score
        intelligence = financial_intelligence_score(
            snapshot=bundle.snapshot,
            income_insights=insights["income"],
            trend_insights=insights["trends"],
            habits=insights["habits"],
            forecast=insights["forecast"],
            goal_insights=insights["goals"],
            settings=self.settings
        )

        logger.info("Pipeline completed successfully")

        return FISReport(intelligence=intelligence, insights=insights)
