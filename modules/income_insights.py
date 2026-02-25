import numpy as np
from typing import List, Dict, Any
from .core import MonthlyLogEntry


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
    """
    Converts percentage change into a 0–100 strength score.
    """
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
# Seasonality Detection
# =====================================================

def _detect_seasonality(entries: List[MonthlyLogEntry]) -> float:
    """
    Detects repeating income cycles (e.g., bi-weekly paychecks).
    Returns a value between 0 and 1.
    """

    if len(entries) < 4:
        return 0.0

    incomes = np.array([e.income for e in entries])
    diffs = np.diff(incomes)

    # Strong seasonality = repeating up/down pattern
    sign_changes = np.sum(np.sign(diffs[:-1]) != np.sign(diffs[1:]))

    seasonality_strength = min(1.0, sign_changes / len(diffs))
    return round(seasonality_strength, 3)


# =====================================================
# Income Trend Analysis
# =====================================================

def income_trend(entries: List[MonthlyLogEntry], months: int = 3) -> Dict[str, Any]:
    if len(entries) < 2:
        return {
            "slope": 0.0,
            "direction": "No trend",
            "rate_pct": 0.0,
            "strength": 0
        }

    last_entries = entries[-months:] if len(entries) >= months else entries

    xs = [e.month_index for e in last_entries]
    ys = [float(e.income) for e in last_entries]

    slope_val = _slope(xs, ys)

    # Direction
    if slope_val > 0:
        direction = "Increasing"
    elif slope_val < 0:
        direction = "Decreasing"
    else:
        direction = "Stable"

    # Percentage change
    if ys[0] > 0:
        rate_pct = ((ys[-1] - ys[0]) / ys[0]) * 100
    else:
        rate_pct = 0.0

    strength = _trend_strength(rate_pct)

    return {
        "slope": round(slope_val, 2),
        "direction": direction,
        "rate_pct": round(rate_pct, 2),
        "strength": strength
    }


# =====================================================
# Income Stability (Coefficient of Variation)
# =====================================================

def income_stability(entries: List[MonthlyLogEntry], months: int = 3) -> float:
    if len(entries) < 2:
        return 0.0

    last_entries = entries[-months:] if len(entries) >= months else entries
    incomes = np.array([float(e.income) for e in last_entries])

    mean = incomes.mean()
    std = incomes.std()

    stability = std / mean if mean > 0 else 0.0
    return round(stability, 3)


# =====================================================
# Income Forecasting
# =====================================================

def income_forecast(entries: List[MonthlyLogEntry]) -> float:
    """
    Simple linear projection using slope.
    """
    if len(entries) < 2:
        return entries[-1].income if entries else 0.0

    xs = [e.month_index for e in entries]
    ys = [float(e.income) for e in entries]

    slope_val = _slope(xs, ys)
    next_month = ys[-1] + slope_val

    return round(next_month, 2)


# =====================================================
# Income Reliability Score (0–100)
# =====================================================

def _income_reliability(stability: float, trend_strength: int, seasonality: float) -> int:
    """
    Combines stability, trend strength, and seasonality into a reliability score.
    """

    score = 0

    # Stability (lower volatility = better)
    if stability < 0.05:
        score += 40
    elif stability < 0.15:
        score += 25
    elif stability < 0.30:
        score += 10

    # Trend strength
    score += trend_strength * 0.4  # up to 40 points

    # Seasonality helps predictability
    score += seasonality * 20  # up to 20 points

    return min(100, int(score))


# =====================================================
# Income Health Classification
# =====================================================

def _income_health(reliability: int, trend_direction: str) -> str:
    if reliability >= 80 and trend_direction == "Increasing":
        return "Strong & Growing"
    if reliability >= 60:
        return "Stable"
    if reliability >= 40:
        return "Volatile"
    if trend_direction == "Decreasing":
        return "Declining"
    return "Uncertain"


# =====================================================
# Combined Income Insights
# =====================================================

def income_summary(entries: List[MonthlyLogEntry], months: int = 3) -> Dict[str, Any]:
    trend = income_trend(entries, months)
    stability = income_stability(entries, months)
    seasonality = _detect_seasonality(entries)
    forecast = income_forecast(entries)

    reliability = _income_reliability(
        stability=stability,
        trend_strength=trend["strength"],
        seasonality=seasonality
    )

    health = _income_health(
        reliability=reliability,
        trend_direction=trend["direction"]
    )

    return {
        "trend": trend,
        "stability": stability,
        "seasonality": seasonality,
        "forecast_next_month": forecast,
        "reliability_score": reliability,
        "income_health": health
    }