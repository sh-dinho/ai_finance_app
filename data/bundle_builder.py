from datetime import datetime
from typing import Dict
from core.models import MonthlyLogEntry, Goal, FinancialDataBundle
from core.snapshot import FinancialSnapshot
from .validators import validate_monthly_entries, validate_daily_dataframe


def build_monthly_entries(df) -> list:
    entries = []
    for _, row in df.iterrows():
        entries.append(
            MonthlyLogEntry(
                month=row.get("month", ""),
                income=row.get("income", 0.0),
                expenses=row.get("expenses", 0.0),
                savings=row.get("savings", 0.0),
            )
        )
    return entries


def build_goals(raw_goals: Dict[str, Dict]) -> Dict[str, Goal]:
    goals = {}
    for name, g in raw_goals.items():
        goals[name] = Goal(
            name=name,
            target=g.get("target", 0.0),
            target_date=datetime.strptime(g.get("target_date"), "%Y-%m-%d").date(),
        )
    return goals


def build_bundle(settings, df_monthly, df_daily, raw_goals, current_values) -> FinancialDataBundle:
    entries = build_monthly_entries(df_monthly)
    validate_monthly_entries(entries)

    validate_daily_dataframe(df_daily)

    snapshot = FinancialSnapshot.from_raw(
        monthly_income=entries[-1].income if entries else 0.0,
        monthly_expenses=entries[-1].expenses if entries else 0.0,
        investments=current_values.get("investments", 0.0),
        liquid_assets=current_values.get("liquid_assets", 0.0),
        debt=current_values.get("debt", 0.0),
        emergency_fund=current_values.get("emergency_fund", 0.0),
        has_high_interest_debt=current_values.get("has_high_interest_debt", False),
        income_history=[e.income for e in entries],
        expense_history=[e.expenses for e in entries],
    )

    goals = build_goals(raw_goals)

    return FinancialDataBundle(
        snapshot=snapshot,
        entries=entries,
        df_daily=df_daily,
        goals=goals,
        current_goal_values=current_values,
        monthly_savings=snapshot.savings_amount,
    )
