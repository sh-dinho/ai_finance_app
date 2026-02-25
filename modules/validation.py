# modules/validation.py
from typing import Dict, Any, List
import pandas as pd

from .core import FinancialSnapshot, MonthlyLogEntry
from .models import FinancialDataBundle


def validate_daily_df(df: pd.DataFrame) -> None:
    required_cols = {"date", "expenses"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"df_daily is missing required columns: {missing}")


def validate_entries(entries: List[MonthlyLogEntry]) -> None:
    if not entries:
        raise ValueError("entries list is empty")
    # Ensure sorted by month_index
    if any(entries[i].month_index > entries[i + 1].month_index for i in range(len(entries) - 1)):
        raise ValueError("entries must be sorted by month_index")


def validate_goals(goals: Dict[str, Dict[str, Any]], current_values: Dict[str, float]) -> None:
    for name, g in goals.items():
        if "target" not in g:
            raise ValueError(f"Goal '{name}' missing 'target'")
    # current_values can be sparse; that's fine


def validate_snapshot(snapshot: FinancialSnapshot) -> None:
    if snapshot.monthly_income < 0 or snapshot.monthly_expenses < 0:
        raise ValueError("Income/expenses cannot be negative")
    if snapshot.emergency_months < 0:
        raise ValueError("emergency_months cannot be negative")


def validate_bundle(bundle: FinancialDataBundle) -> None:
    validate_snapshot(bundle.snapshot)
    validate_entries(bundle.entries)
    validate_daily_df(bundle.df_daily)
    validate_goals(bundle.goals, bundle.current_goal_values)