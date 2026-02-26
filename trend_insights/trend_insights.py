import pandas as pd

def trend_summary(entries: list) -> dict:
    """
    Computes monthly trends for income, expenses, and savings
    from MonthlyLogEntry objects.
    """

    if not entries:
        return {"error": "No entries provided"}

    # Build DataFrame from MonthlyLogEntry fields
    df = pd.DataFrame([{
        "month": e.month,
        "income": e.income,
        "expenses": e.expenses,
        "savings": e.savings
    } for e in entries])

    # Convert "YYYY-MM" to datetime for sorting
    df["date"] = pd.to_datetime(df["month"], format="%Y-%m")
    df = df.sort_values("date")

    metrics = ["income", "expenses", "savings"]
    results = {}

    for metric in metrics:
        series = df.set_index("date")[metric]

        if len(series) < 2:
            results[metric] = {"error": "Not enough data for trend analysis"}
            continue

        mom_change = series.pct_change().fillna(0)
        rolling = series.rolling(3).mean().fillna(method="bfill")

        results[metric] = {
            "monthly_totals": series.astype(float).to_dict(),
            "month_over_month_change": mom_change.astype(float).to_dict(),
            "rolling_3_month_average": rolling.astype(float).to_dict(),
            "latest_month_total": float(series.iloc[-1]),
            "trend_direction": "up" if series.iloc[-1] > series.iloc[-2] else "down"
        }

    return results