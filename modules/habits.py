import pandas as pd
import numpy as np
from typing import Dict, Any


# =====================================================
# Logging Streak (Calendar Accurate)
# =====================================================

def calculate_logging_streak(df: pd.DataFrame, allowed_gap_days: int = 2) -> int:
    """
    Calculates consecutive logging days, allowing small gaps.
    """
    if df.empty or "date" not in df.columns:
        return 0

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    if df.empty:
        return 0

    unique_days = df["date"].dt.date.drop_duplicates().sort_values()

    # If user hasn't logged today or yesterday, streak may have ended
    last_day = unique_days.iloc[-1]
    today = pd.Timestamp.today().date()
    if (today - last_day).days > allowed_gap_days:
        return 0

    streak = 1
    for i in range(len(unique_days) - 1, 0, -1):
        diff = (unique_days.iloc[i] - unique_days.iloc[i - 1]).days
        if diff <= allowed_gap_days:
            streak += 1
        else:
            break

    return streak


# =====================================================
# Savings Streak (Strict Positive Savings)
# =====================================================

def calculate_savings_streak(df: pd.DataFrame, threshold: float = 0.01) -> int:
    """
    Counts consecutive periods with positive savings.
    Ignores tiny noise values.
    """
    if df.empty or "savings" not in df.columns:
        return 0

    df = df.copy()
    df["savings"] = pd.to_numeric(df["savings"], errors="coerce").fillna(0)

    streak = 0
    for value in reversed(df["savings"].tolist()):
        if value > threshold:
            streak += 1
        else:
            break

    return streak


# =====================================================
# Strong Savings Streak (Savings Rate Based)
# =====================================================

def calculate_strong_savings_streak(df: pd.DataFrame, min_rate: float = 0.10) -> int:
    """
    Counts consecutive periods where savings rate meets or exceeds a threshold.
    """
    if df.empty or "income" not in df.columns or "expenses" not in df.columns:
        return 0

    df = df.copy()
    df["income"] = pd.to_numeric(df["income"], errors="coerce").fillna(0)
    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce").fillna(0)

    df["savings_rate"] = ((df["income"] - df["expenses"]) / df["income"]) \
        .replace([float("inf"), -float("inf")], 0).fillna(0)

    streak = 0
    for rate in reversed(df["savings_rate"].tolist()):
        if rate >= min_rate:
            streak += 1
        else:
            break

    return streak


# =====================================================
# Habit Consistency Score (0–100)
# =====================================================

def consistency_score(logging_streak: int, savings_streak: int, strong_savings_streak: int) -> Dict[str, Any]:
    """
    Weighted behavior score combining logging consistency,
    savings consistency, and strong savings behavior.
    """
    score = (
        logging_streak * 4 +
        savings_streak * 3 +
        strong_savings_streak * 5
    )

    score = min(100, score)

    if score < 40:
        status = "Weak"
    elif score < 70:
        status = "Moderate"
    else:
        status = "Excellent"

    return {
        "score": score,
        "status": status
    }


# =====================================================
# Momentum Indicator
# =====================================================

def habit_momentum(df: pd.DataFrame) -> str:
    """
    Detects improvement or decline in recent savings behavior.
    """
    if df.empty or "savings" not in df.columns:
        return "Neutral"

    df = df.copy()
    df["savings"] = pd.to_numeric(df["savings"], errors="coerce").fillna(0)

    if len(df) < 6:
        return "Neutral"

    recent_avg = df["savings"].tail(3).mean()
    previous_avg = df["savings"].iloc[-6:-3].mean()

    if recent_avg > previous_avg:
        return "Improving"
    elif recent_avg < previous_avg:
        return "Declining"
    else:
        return "Stable"