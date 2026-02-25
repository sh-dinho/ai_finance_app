# modules/loaders.py
from typing import Dict, Any, List
import json
import pandas as pd
from datetime import date
from .core import MonthlyLogEntry, FinancialSnapshot
from .goals import load_goals


def load_daily_transactions_from_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def load_monthly_entries_from_csv(path: str) -> List[MonthlyLogEntry]:
    df = pd.read_csv(path)
    entries: List[MonthlyLogEntry] = []
    for _, row in df.iterrows():
        entries.append(
            MonthlyLogEntry(
                month_index=int(row["month_index"]),
                income=float(row["income"]),
                expenses=float(row["expenses"]),
                savings=float(row.get("savings", row["income"] - row["expenses"]))
            )
        )
    return entries


def load_snapshot_from_json(path: str) -> FinancialSnapshot:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return FinancialSnapshot(**raw)


def load_goals_and_values(goals_path: str, values_path: str) -> tuple[Dict[str, Dict[str, Any]], Dict[str, float]]:
    goals = load_goals(goals_path)
    with open(values_path, "r", encoding="utf-8") as f:
        current_values = json.load(f)
    return goals, {k: float(v) for k, v in current_values.items()}