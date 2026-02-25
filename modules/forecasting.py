import pandas as pd
import numpy as np
from typing import Dict, Any


# =====================================================
# Expense Forecasting Engine (Enhanced)
# =====================================================

def forecast_expenses(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Forecast next-week and next-month expenses using:
    - Daily aggregation
    - Rolling averages (7d, 30d)
    - Trend multiplier (adaptive regression)
    - Seasonality detection
    - Volatility-adjusted confidence score
    - Forecast quality score
    """

    if df.empty or "date" not in df.columns or "expenses" not in df.columns:
        return _empty_forecast()

    df = df.copy()

    # Clean data
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce").fillna(0)
    df = df.dropna(subset=["date"]).sort_values("date")

    if df.empty:
        return _empty_forecast()

    # -------------------------------------------------
    # Daily aggregation
    # -------------------------------------------------
    daily = (
        df.groupby(df["date"].dt.date)["expenses"]
        .sum()
        .reset_index()
    )

    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date")

    # Require at least 7 days of data
    if len(daily) < 7:
        return _empty_forecast(min_data=True)

    # -------------------------------------------------
    # Outlier-resistant smoothing
    # -------------------------------------------------
    daily["smoothed"] = daily["expenses"].rolling(
        window=5, center=True, min_periods=1
    ).median()

    # -------------------------------------------------
    # Rolling averages
    # -------------------------------------------------
    daily["7d_avg"] = daily["smoothed"].rolling(window=7, min_periods=3).mean()
    daily["30d_avg"] = daily["smoothed"].rolling(window=30, min_periods=7).mean()

    latest_7d = daily["7d_avg"].iloc[-1] if not daily["7d_avg"].empty else 0
    latest_30d = daily["30d_avg"].iloc[-1] if not daily["30d_avg"].empty else 0

    latest_7d = 0 if np.isnan(latest_7d) else latest_7d
    latest_30d = 0 if np.isnan(latest_30d) else latest_30d

    # -------------------------------------------------
    # Trend Detection (Adaptive)
    # -------------------------------------------------
    trend_multiplier = _calculate_trend_multiplier(daily)

    next_week = latest_7d * 7 * trend_multiplier
    next_month = latest_30d * 30 * trend_multiplier

    # -------------------------------------------------
    # Seasonality Detection
    # -------------------------------------------------
    seasonality_strength = _detect_seasonality(daily)

    # -------------------------------------------------
    # Volatility & Confidence
    # -------------------------------------------------
    volatility_ratio = _calculate_volatility_ratio(daily["expenses"])
    confidence = max(0.05, min(1.0, 1 - volatility_ratio))

    # -------------------------------------------------
    # Forecast Quality Score
    # -------------------------------------------------
    quality = _forecast_quality(
        data_len=len(daily),
        volatility=volatility_ratio,
        seasonality=seasonality_strength,
        trend_multiplier=trend_multiplier
    )

    return {
        "next_week": round(next_week, 2),
        "next_month": round(next_month, 2),
        "trend_multiplier": round(trend_multiplier, 3),
        "volatility_ratio": round(volatility_ratio, 3),
        "seasonality_strength": round(seasonality_strength, 3),
        "confidence": round(confidence, 2),
        "forecast_quality": quality
    }


# =====================================================
# Helper: Trend Multiplier (Adaptive)
# =====================================================

def _calculate_trend_multiplier(daily: pd.DataFrame) -> float:
    """
    Detects spending trend using linear regression slope.
    Trend impact increases with dataset length.
    """

    if len(daily) < 10:
        return 1.0

    y = daily["smoothed"].values
    x = np.arange(len(y))

    slope = np.polyfit(x, y, 1)[0]

    if abs(slope) < 0.01:
        return 1.0

    mean_y = max(y.mean(), 1)

    # Adaptive scaling: more data = stronger trend effect
    scale = min(1.5, len(daily) / 30)

    trend_factor = 1 + (slope / mean_y) * 5 * scale

    return max(0.85, min(1.15, trend_factor))


# =====================================================
# Helper: Seasonality Detection
# =====================================================

def _detect_seasonality(daily: pd.DataFrame) -> float:
    """
    Detects weekly seasonality by comparing weekday vs weekend averages.
    Returns a value between 0 and 1.
    """

    daily["weekday"] = daily["date"].dt.weekday
    weekend = daily[daily["weekday"] >= 5]["expenses"].mean()
    weekday = daily[daily["weekday"] < 5]["expenses"].mean()

    if weekday == 0:
        return 0.0

    diff_ratio = abs(weekend - weekday) / weekday
    return min(1.0, diff_ratio)


# =====================================================
# Helper: Volatility Ratio (MAD)
# =====================================================

def _calculate_volatility_ratio(expenses: pd.Series) -> float:
    mean = expenses.mean()
    if mean <= 0:
        return 0

    mad = np.median(np.abs(expenses - np.median(expenses)))
    return float(mad / mean)


# =====================================================
# Forecast Quality Score
# =====================================================

def _forecast_quality(data_len: int, volatility: float, seasonality: float, trend_multiplier: float) -> str:
    """
    Produces a human-friendly quality rating.
    """

    score = 0

    # More data = better
    if data_len >= 60:
        score += 40
    elif data_len >= 30:
        score += 25
    elif data_len >= 14:
        score += 10

    # Lower volatility = better
    if volatility < 0.2:
        score += 30
    elif volatility < 0.4:
        score += 15

    # Seasonality helps predictability
    if seasonality > 0.3:
        score += 10

    # Trend stability
    if 0.95 <= trend_multiplier <= 1.05:
        score += 20

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    return "Low"


# =====================================================
# Empty Forecast
# =====================================================

def _empty_forecast(min_data: bool = False) -> Dict[str, Any]:
    return {
        "next_week": 0,
        "next_month": 0,
        "trend_multiplier": 1.0,
        "volatility_ratio": 0,
        "seasonality_strength": 0,
        "confidence": 0,
        "forecast_quality": "Insufficient Data" if min_data else "Low"
    }