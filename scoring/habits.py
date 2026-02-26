import pandas as pd
from scoring.utils import clamp, pct


def calculate_consistency_metrics(df_daily: pd.DataFrame, entries):
    if df_daily is None or df_daily.empty:
        return {"status": "Unknown", "score": 0}

    df = df_daily.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Example habit: spending under control
    if "spending" in df.columns:
        avg_spending = df["spending"].mean()
        std_spending = df["spending"].std() or 0
        stability = clamp(100 - pct(std_spending, avg_spending))
    else:
        stability = 50

    # Example habit: income stability
    incomes = [e.income for e in entries]
    income_stability = clamp(100 - pct(max(incomes) - min(incomes), max(incomes)))

    score = clamp((stability + income_stability) / 2)

    status = (
        "Excellent" if score >= settings.thresholds.habits.excellent
        else "Moderate" if score >= settings.thresholds.habits.moderate
        else "Weak"
    )

    return {
        "stability": stability,
        "income_stability": income_stability,
        "score": score,
        "status": status,
    }
