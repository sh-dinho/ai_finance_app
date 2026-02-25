import random
import pandas as pd
from datetime import date, timedelta
from typing import List, Dict, Any, Tuple

from .utils import (
    random_with_volatility, apply_trend,
    apply_seasonality, pick_life_events
)
from modules.core import MonthlyLogEntry, FinancialSnapshot
from modules.goals import Goal


class PersonaBase:
    def generate(self, profile: Dict[str, Any], months: int = 24) -> Dict[str, Any]:
        """Orchestrates the generation of a full financial history."""
        monthly = self.generate_monthly_entries(profile, months)
        daily = self.generate_daily_data(profile, monthly)
        snapshot = self.generate_snapshot(profile, monthly)
        goals, current_values = self.generate_goals(profile)

        return {
            "snapshot": snapshot,
            "entries": monthly,
            "df_daily": daily,
            "goals": goals,
            "current_goal_values": current_values,
            "monthly_savings": snapshot.monthly_income - snapshot.monthly_expenses,
            "age": random.randint(*profile.get("age_range", (25, 45))),
        }

    def generate_monthly_entries(self, profile: Dict[str, Any], months: int) -> List[MonthlyLogEntry]:
        entries = []
        life_events = pick_life_events(profile.get("life_events", {}), months)

        # Track life events by month for easy lookup
        event_map = {m: ev for ev, m in life_events}

        for m in range(months):
            income = random_with_volatility(profile["income_base"], profile["income_volatility"])
            income = apply_trend(income, m, profile["income_trend"])

            expenses = random_with_volatility(profile["expense_base"], profile["expense_volatility"])

            # Apply life event impacts
            if m in event_map:
                event_name = event_map[m]
                if "spike" in event_name or "bonus" in event_name:
                    income *= 1.5
                if "repair" in event_name or "vacation" in event_name:
                    expenses *= 1.3

            entries.append(MonthlyLogEntry(
                month_index=m,
                income=round(income, 2),
                expenses=round(expenses, 2),
                savings=round(max(0, income - expenses), 2)
            ))
        return entries

    def generate_snapshot(self, profile: Dict[str, Any], monthly_entries: List[MonthlyLogEntry]) -> FinancialSnapshot:
        """
        FIXED: Converts categorical trends ('up', 'down') into numeric multipliers
        to ensure compatibility with FinancialEngine scoring.
        """
        last_month = monthly_entries[-1]

        # Map string trends to numeric values for the Intelligence Engine
        trend_map = {"increasing": 1.05, "decreasing": 0.95, "flat": 1.0}

        return FinancialSnapshot(
            savings_rate=(last_month.income - last_month.expenses) / last_month.income if last_month.income > 0 else 0,
            monthly_income=last_month.income,
            monthly_expenses=last_month.expenses,
            emergency_months=random.uniform(2, 6),
            investments=random.uniform(5000, 50000),
            has_high_interest_debt=random.random() < 0.2,
            liquid_assets_to_debt=random.uniform(0.5, 3.0),
            expense_trend=trend_map.get(profile.get("expense_trend", "flat"), 1.0),
            income_trend=trend_map.get(profile.get("income_trend", "flat"), 1.0),
            income_stability=0.9 if profile.get("income_volatility", 0) < 0.1 else 0.6
        )

    def generate_daily_data(self, profile: Dict[str, Any], monthly_entries: List[MonthlyLogEntry]) -> pd.DataFrame:
        """Generates synthetic daily transaction records."""
        records = []
        start_date = date.today() - timedelta(days=len(monthly_entries) * 30)

        for entry in monthly_entries:
            daily_expense = entry.expenses / 30
            for d in range(30):
                records.append({
                    "date": start_date + timedelta(days=entry.month_index * 30 + d),
                    "expenses": random_with_volatility(daily_expense, 0.2),
                    "income": entry.income / 2 if d in [1, 15] else 0  # Bi-monthly pay
                })
        return pd.DataFrame(records)

    def generate_goals(self, profile: Dict[str, Any]) -> Tuple[Dict[str, Goal], Dict[str, float]]:
        goals = {}
        current_vals = {}
        for name, target, years in profile.get("goals", []):
            goals[name] = Goal(name=name, target=target, target_date=date.today() + timedelta(days=years * 365))
            current_vals[name] = random.uniform(0, target * 0.3)
        return goals, current_vals