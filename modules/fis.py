# modules/fis.py
from typing import Dict, Any, List
import pandas as pd

from .core import FinancialSnapshot, MonthlyLogEntry
from .financial_engine import FinancialEngine
from .discipline_risk import calculate_discipline_risk
from .income_insights import income_summary
from .trend_insights import trend_summary
from .forecasting import forecast_expenses
from .habits import (
    calculate_logging_streak,
    calculate_savings_streak,
    calculate_strong_savings_streak,
    consistency_score,
    habit_momentum
)
from .goals import calculate_all_goals_progress
from .goals_recommendations import generate_goal_insights
from .financial_intelligence_score import financial_intelligence_score
from .models import FinancialDataBundle, FISReport
from .validation import validate_bundle


def generate_fis_report(
    snapshot: FinancialSnapshot,
    entries: List[MonthlyLogEntry],
    df_daily: pd.DataFrame,
    goals: Dict[str, Dict[str, Any]],
    current_goal_values: Dict[str, float],
    budget_comparison: Dict[str, Any] | None = None,
    age: int = 30,
    monthly_savings: float = 0.0
) -> Dict[str, Any]:
    ratios = FinancialEngine.calculate_ratios(snapshot)
    emergency_status = FinancialEngine.emergency_fund_status(snapshot)
    goal_progress = calculate_all_goals_progress(goals, current_goal_values)

    income_insights = income_summary(entries)
    trend_insights = trend_summary(entries)
    forecast = forecast_expenses(df_daily)
    discipline_risk = calculate_discipline_risk(df_daily, budget_comparison)

    logging_streak = calculate_logging_streak(df_daily)
    savings_streak = calculate_savings_streak(df_daily)
    strong_savings_streak = calculate_strong_savings_streak(df_daily)

    habits = {
        "logging_streak": logging_streak,
        "savings_streak": savings_streak,
        "strong_savings_streak": strong_savings_streak,
        "consistency": consistency_score(logging_streak, savings_streak, strong_savings_streak),
        "momentum": habit_momentum(df_daily)
    }

    goal_insights = generate_goal_insights(
        goals=goals,
        current_values=current_goal_values,
        monthly_savings=monthly_savings
    )

    intelligence_score = financial_intelligence_score(
        snapshot=snapshot,
        income_insights=income_insights,
        trend_insights=trend_insights,
        habits=habits,
        forecast=forecast,
        goal_insights=goal_insights
    )

    return {
        "ratios": ratios,
        "emergency_fund": emergency_status,
        "income_insights": income_insights,
        "trend_insights": trend_insights,
        "forecast": forecast,
        "discipline_risk": discipline_risk,
        "habits": habits,
        "goals": goal_progress,
        "goal_insights": goal_insights,
        "intelligence_score": intelligence_score
    }


def generate_fis_report_from_bundle(bundle: FinancialDataBundle) -> FISReport:
    validate_bundle(bundle)

    raw = generate_fis_report(
        snapshot=bundle.snapshot,
        entries=bundle.entries,
        df_daily=bundle.df_daily,
        goals=bundle.goals,
        current_goal_values=bundle.current_goal_values,
        budget_comparison=bundle.budget_comparison,
        age=bundle.age,
        monthly_savings=bundle.monthly_savings
    )

    return FISReport(
        ratios=raw["ratios"],
        emergency_fund=raw["emergency_fund"],
        income_insights=raw["income_insights"],
        trend_insights=raw["trend_insights"],
        forecast=raw["forecast"],
        discipline_risk=raw["discipline_risk"],
        habits=raw["habits"],
        goals=raw["goals"],
        goal_insights=raw["goal_insights"],
        intelligence_score=raw["intelligence_score"]
    )