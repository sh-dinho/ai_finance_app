# modules/loaders.py

import json
import logging
from typing import Dict, Any, List, Tuple
from datetime import date
import pandas as pd

from .core import MonthlyLogEntry, FinancialSnapshot
from .goals import load_goals

logger = logging.getLogger(__name__)


# =====================================================
# Load Daily Transactions
# =====================================================

def load_daily_transactions_from_csv(path: str) -> pd.DataFrame:
    """
    Load raw daily transactions from CSV.
    Expected columns: date, income?, expenses?, savings?
    """
    logger.debug(f"Loading daily transactions from: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        logger.error(f"Failed to load daily transactions CSV: {e}")
        return pd.DataFrame()

    if "date" not in df.columns:
        logger.warning("Daily transactions CSV missing 'date' column")

    return df


# =====================================================
# Load Monthly Log Entries
# =====================================================

def load_monthly_entries_from_csv(path: str) -> List[MonthlyLogEntry]:
    """
    Load monthly financial entries and convert to MonthlyLogEntry dataclasses.
    Expected columns: month_index, income, expenses, (optional) savings
    """
    logger.debug(f"Loading monthly entries from: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        logger.error(f"Failed to load monthly entries CSV: {e}")
        return []

    required_cols = {"month_index", "income", "expenses"}
    missing = required_cols - set(df.columns)
    if missing:
        logger.error(f"Monthly entries CSV missing required columns: {missing}")
        return []

    entries: List[MonthlyLogEntry] = []

    for _, row in df.iterrows():
        try:
            income = float(row["income"])
            expenses = float(row["expenses"])
            savings = float(row.get("savings", income - expenses))

            entry = MonthlyLogEntry(
                month_index=int(row["month_index"]),
                income=income,
                expenses=expenses,
                savings=savings
            )
            entries.append(entry)

        except Exception as e:
            logger.warning(f"Skipping malformed monthly entry row: {row} — {e}")

    logger.info(f"Loaded {len(entries)} monthly entries")
    return entries


# =====================================================
# Load Financial Snapshot
# =====================================================

def load_snapshot_from_json(path: str) -> FinancialSnapshot:
    """
    Load a FinancialSnapshot from JSON.
    """
    logger.debug(f"Loading financial snapshot from: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load snapshot JSON: {e}")
        raise

    try:
        snapshot = FinancialSnapshot(**raw)
    except Exception as e:
        logger.error(f"Malformed snapshot JSON structure: {e}")
        raise

    logger.info("Financial snapshot loaded successfully")
    return snapshot


# =====================================================
# Load Goals + Current Values
# =====================================================

def load_goals_and_values(
    goals_path: str,
    values_path: str
) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
    Load goals (Goal dataclasses) and current values (floats).
    """
    logger.debug(f"Loading goals from: {goals_path}")
    goals = load_goals(goals_path)

    logger.debug(f"Loading goal current values from: {values_path}")
    try:
        with open(values_path, "r", encoding="utf-8") as f:
            raw_values = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load goal values JSON: {e}")
        return goals, {}

    current_values = {}
    for k, v in raw_values.items():
        try:
            current_values[k] = float(v)
        except Exception:
            logger.warning(f"Invalid goal value for '{k}': {v}")

    logger.info(f"Loaded {len(goals)} goals and {len(current_values)} current values")
    return goals, current_values