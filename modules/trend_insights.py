from typing import List, Dict, Any
from .core import MonthlyLogEntry
import numpy as np


# =====================================================
# Helper: Slope (Least Squares)
# =====================================================

def _slope(xs: List[float], ys: List[float]) -> float:
    n = len(xs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denominator = sum((x - x_mean) ** 2 for x in xs) or 1e-9

    return numerator / denominator


# =====================================================
# Trend Strength (0–100)
# =====================================================

def _trend_strength(rate_pct: float) -> int:
    abs_rate = abs(rate_pct)

    if abs_rate >= 20:
        return 100
    elif abs_rate >= 10:
        return 70
    elif abs_rate >= 5:
        return 40
    elif abs_rate >= 1:
        return 20
    return 5


# =====================================================
# Volatility (Coefficient of Variation)
# =====================================================

def _volatility(values: List[float]) -> float:
    arr = np.array(values, dtype=float)
    mean = arr.mean()
    std = arr.std()
    return round(std / mean, 3) if mean > 0 else 0.0


# =====================================================
# Forecast Next Month
# =====================================================

def _forecast_next(ys: List[float], slope_val: float) -> float:
    return round(ys[-1] + slope_val, 2)


# =====================================================
# Expense Trend
# =====================================================

def expense_trend(entries: List[MonthlyLogEntry], months: int = 3) -> Dict[str, Any]:
    if len(entries) < 2:
        return {
            "slope": 0.0,
            "direction": "No trend",
            "rate_pct": 0.0,
            "strength": 0,
            "volatility": 0.0,
            "forecast_next_month": 0.0,
            "health": "Unknown"
        }

    last_entries = entries[-months:] if len(entries) >= months else entries

    xs = [e.month_index for e in last_entries]
    ys = [float(e.expenses) for e in last_entries]

    slope_val = _slope(xs, ys)

    direction = (
        "Increasing" if slope_val > 0
        else "Decreasing" if slope_val < 0
        else "Stable"
    )

    rate_pct = ((ys[-1] - ys[0]) / ys[0] * 100) if ys[0] != 0 else 0.0
    strength = _trend_strength(rate_pct)
    vol = _volatility(ys)
    forecast = _forecast_next(ys, slope_val)

    # Health classification
    if direction == "Decreasing" and vol < 0.1:
        health = "Improving"
    elif direction == "Increasing" and strength > 40:
        health = "Worsening"
    elif vol > 0.3:
        health = "Volatile"
    else:
        health = "Stable"

    return {
        "slope": round(slope_val, 2),
        "direction": direction,
        "rate_pct": round(rate_pct, 2),
        "strength": strength,
        "volatility": vol,
        "forecast_next_month": forecast,
        "health": health
    }


# =====================================================
# Savings Trend
# =====================================================

def savings_trend(entries: List[MonthlyLogEntry], months: int = 3) -> Dict[str, Any]:
    if len(entries) < 2:
        return {
            "slope": 0.0,
            "direction": "No trend",
            "rate_pct": 0.0,
            "strength": 0,
            "volatility": 0.0,
            "forecast_next_month": 0.0,
            "health": "Unknown"
        }

    last_entries = entries[-months:] if len(entries) >= months else entries

    xs = [e.month_index for e in last_entries]
    ys = [float(e.savings) for e in last_entries]

    slope_val = _slope(xs, ys)

    direction = (
        "Increasing" if slope_val > 0
        else "Decreasing" if slope_val < 0
        else "Stable"
    )

    rate_pct = ((ys[-1] - ys[0]) / ys[0] * 100) if ys[0] != 0 else 0.0
    strength = _trend_strength(rate_pct)
    vol = _volatility(ys)
    forecast = _forecast_next(ys, slope_val)

    # Health classification
    if direction == "Increasing" and strength > 40:
        health = "Strong"
    elif direction == "Decreasing":
        health = "Weakening"
    elif vol > 0.3:
        health = "Volatile"
    else:
        health = "Stable"

    return {
        "slope": round(slope_val, 2),
        "direction": direction,
        "rate_pct": round(rate_pct, 2),
        "strength": strength,
        "volatility": vol,
        "forecast_next_month": forecast,
        "health": health
    }


# =====================================================
# Combined Trend Summary
# =====================================================

def trend_summary(entries: List[MonthlyLogEntry]) -> Dict[str, Any]:
    return {
        "expense_trend": expense_trend(entries),
        "savings_trend": savings_trend(entries)
    }