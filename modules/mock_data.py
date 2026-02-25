# modules/mock_data.py
from typing import Dict, Any, List
from datetime import date, timedelta
import pandas as pd
import random

from .core import FinancialSnapshot, MonthlyLogEntry
from .models import FinancialDataBundle


def generate_mock_data(months: int = 6) -> FinancialDataBundle:
    today = date.today()
    entries: List[MonthlyLogEntry] = []
    df_rows = []

    base_income = 5000
    base_expenses = 3500

    for i in range(months):
        income = base_income + random.randint(-300, 300)
        expenses = base_expenses + random.randint(-400, 400)
        savings = income - expenses
        entries.append(
            MonthlyLogEntry(
                month_index=i,
                income=income,
                expenses=expenses,
                savings=savings
            )
        )

    # Daily data (last 60 days)
    for d in range(60):
        day = today - timedelta(days=59 - d)
        expenses = max(0, base_expenses / 30 + random.randint(-40, 40))
        income = base_income / 30 if d % 15 == 0 else 0
        savings = income - expenses
        df_rows.append(
            {"date": day, "income": income, "expenses": expenses, "savings": savings}
        )

    df_daily = pd.DataFrame(df_rows)

    snapshot = FinancialSnapshot(
        monthly_income=base_income,
        monthly_expenses=base_expenses,
        savings_rate=(base_income - base_expenses) / base_income,
        emergency_months=2.5,
        has_high_interest_debt=True,
        liquid_assets_to_debt=0.4,
        investments=10000
    )

    goals: Dict[str, Dict[str, Any]] = {
        "Emergency Fund": {"target": 15000.0, "target_date": today.replace(year=today.year + 2)},
        "Vacation": {"target": 3000.0, "target_date": today.replace(year=today.year + 1)},
    }
    current_goal_values: Dict[str, float] = {
        "Emergency Fund": 4000.0,
        "Vacation": 500.0
    }

    bundle = FinancialDataBundle(
        snapshot=snapshot,
        entries=entries,
        df_daily=df_daily,
        goals=goals,
        current_goal_values=current_goal_values,
        monthly_savings=base_income - base_expenses,
        age=30
    )
    return bundle