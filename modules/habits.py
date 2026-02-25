import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def calculate_consistency_metrics(df_daily: pd.DataFrame, monthly_entries: list) -> Dict[str, Any]:
    """Vectorized habit analysis."""
    if df_daily.empty:
        return {"score": 0, "status": "Weak", "momentum": "Neutral"}

    # 1. Logging Streak
    unique_days = pd.to_datetime(df_daily['date']).dt.date.nunique()
    total_days = (pd.to_datetime(df_daily['date']).max() - pd.to_datetime(df_daily['date']).min()).days + 1
    logging_ratio = unique_days / total_days if total_days > 0 else 0

    # 2. Savings consistency
    savings_vals = np.array([e.savings for e in monthly_entries])
    positive_months = np.sum(savings_vals > 0)
    savings_ratio = positive_months / len(monthly_entries) if monthly_entries else 0

    # 3. Final Score
    raw_score = (logging_ratio * 40) + (savings_ratio * 60)

    return {
        "score": int(raw_score),
        "status": "Excellent" if raw_score > 80 else "Moderate" if raw_score > 50 else "Weak",
        "logging_consistency": round(logging_ratio, 2)
    }