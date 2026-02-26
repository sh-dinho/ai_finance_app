from typing import List
from core.models import MonthlyLogEntry


def validate_monthly_entries(entries: List[MonthlyLogEntry]) -> List[str]:
    errors = []

    for e in entries:
        if e.income < 0:
            errors.append(f"Negative income in {e.month}")
        if e.expenses < 0:
            errors.append(f"Negative expenses in {e.month}")
        if e.savings < 0:
            errors.append(f"Negative savings in {e.month}")
        if e.savings > e.income:
            errors.append(f"Savings exceed income in {e.month}")

    return errors


def validate_daily_dataframe(df):
    if df is None or df.empty:
        return ["Daily dataframe is empty"]
    if "date" not in df.columns:
        return ["Missing 'date' column"]
    return []
