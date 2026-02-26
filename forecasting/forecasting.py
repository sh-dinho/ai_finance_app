# forecasting/forecasting.py

import pandas as pd
import numpy as np

def forecast_expenses(df_daily: pd.DataFrame, periods: int = 30) -> dict:
    """
    Forecast daily expenses using simple exponential smoothing.
    Expects df_daily to contain a column 'expense' or 'amount'.
    """

    if df_daily is None or df_daily.empty:
        return {"error": "No daily data available"}

    # Detect expense column
    expense_col = None
    for col in ["expense", "expenses", "amount", "spend"]:
        if col in df_daily.columns:
            expense_col = col
            break

    if expense_col is None:
        return {"error": "No expense column found"}

    series = df_daily[expense_col].astype(float)

    # Simple exponential smoothing
    alpha = 0.3
    forecast_values = []
    last_value = series.iloc[-1]

    for _ in range(periods):
        next_val = alpha * last_value + (1 - alpha) * series.mean()
        forecast_values.append(next_val)
        last_value = next_val

    return {
        "method": "exponential_smoothing",
        "periods": periods,
        "forecast": forecast_values,
        "average_daily_expense": float(series.mean()),
        "latest_expense": float(series.iloc[-1])
    }