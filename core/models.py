from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import date, datetime
import pandas as pd
import json


@dataclass
class MonthlyLogEntry:
    month: str          # e.g. "2026-01"
    income: float
    expenses: float
    savings: float


@dataclass
class Goal:
    name: str
    target: float
    target_date: date


@dataclass
class FinancialDataBundle:
    snapshot: Any
    entries: List[MonthlyLogEntry]
    df_daily: pd.DataFrame
    goals: Dict[str, Goal]
    current_goal_values: Dict[str, float]
    monthly_savings: float

    @classmethod
    def load_from_source(cls, path: str):
        with open(path, "r") as f:
            raw = json.load(f)

        # Parse entries
        entries = [
            MonthlyLogEntry(
                month=e["month"],
                income=e["income"],
                expenses=e["expenses"],
                savings=e["savings"]
            )
            for e in raw.get("entries", [])
        ]

        # Parse goals
        goals = {
            name: Goal(
                name=name,
                target=g["target"],
                target_date=datetime.strptime(g["target_date"], "%Y-%m-%d").date()
            )
            for name, g in raw.get("goals", {}).items()
        }

        # Daily dataframe
        df_daily = pd.DataFrame(raw.get("df_daily", []))

        return cls(
            snapshot=raw.get("snapshot", {}),
            entries=entries,
            df_daily=df_daily,
            goals=goals,
            current_goal_values=raw.get("current_goal_values", {}),
            monthly_savings=raw.get("monthly_savings", 0.0)
        )