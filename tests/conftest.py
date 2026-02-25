import pytest
import pandas as pd
from datetime import date
from modules.core import FinancialSnapshot, MonthlyLogEntry
from modules.models import FinancialDataBundle
from modules.goals import Goal

@pytest.fixture
def mock_bundle():
    # 1. Setup Snapshot (Your existing logic)
    snapshot = FinancialSnapshot(
        savings_rate=0.2,
        emergency_months=3.0,
        has_high_interest_debt=False,
        liquid_assets_to_debt=1.5,
        expense_trend="stable",
        income_stability=0.9,
        income_trend="flat",
        monthly_expenses=3000.0,
        monthly_income=4000.0,
        emergency_fund=9000.0,
        liquid_assets=15000.0,
        investments=50000.0,
        net_worth=65000.0
    )

    # 2. Add Monthly Entries (Needed for Income/Trend Insights)
    # The pipeline often looks back at the last 3-6 months
    entries = [
        MonthlyLogEntry(month_index=i, income=4000.0, expenses=3000.0, savings=1000.0)
        for i in range(6)
    ]

    # 3. Setup Daily Data (Needed for Forecasting & Habits)
    df_daily = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=30, freq='D'),
        "expenses": [100.0] * 30,
        "income": [0.0] * 29 + [4000.0], # One payday at the end
        "savings": [0.0] * 30
    })

    # 4. Setup Goals (Needed for Goal Intelligence)
    goals = {
        "Emergency Fund": Goal(name="Emergency Fund", target=15000.0, target_date=date(2025, 1, 1))
    }
    current_goal_values = {"Emergency Fund": 9000.0}

    return FinancialDataBundle(
        snapshot=snapshot,
        entries=entries,
        df_daily=df_daily,
        goals=goals,
        current_goal_values=current_goal_values,
        monthly_savings=1000.0,
        age=30
    )