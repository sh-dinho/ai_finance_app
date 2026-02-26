# income_insights/income_insights.py

import pandas as pd
import numpy as np

def income_summary(entries: list) -> dict:
    """
    Summarizes income patterns from a list of transaction-like objects.
    Each entry should have: amount, date, category/type.
    """

    if not entries:
        return {"error": "No income entries"}

    # Extract income-only entries
    income = [e for e in entries if getattr(e, "amount", 0) > 0]

    if not income:
        return {"error": "No positive income entries"}

    amounts = np.array([e.amount for e in income])
    dates = [e.date for e in income]

    return {
        "total_income": float(amounts.sum()),
        "average_income": float(amounts.mean()),
        "income_count": len(amounts),
        "min_income": float(amounts.min()),
        "max_income": float(amounts.max()),
        "income_variance": float(amounts.var()),
        "income_reliability": float(1 / (1 + amounts.var())),  # simple heuristic
        "first_income_date": str(min(dates)),
        "latest_income_date": str(max(dates)),
    }