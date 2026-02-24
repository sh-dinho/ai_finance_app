import json
from pathlib import Path
from typing import Dict
import pandas as pd


# =====================================================
# Load Budgets
# =====================================================

def load_budgets(path: str = "data/budgets.json") -> Dict[str, float]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Budget file not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# Monthly Spending Calculation
# =====================================================

def calculate_monthly_spending(
    df: pd.DataFrame,
    month: str = None
) -> Dict[str, float]:
    """
    Optionally filter by month (YYYY-MM format).
    Requires 'date' and 'category' columns.
    """

    if df.empty or "category" not in df.columns or "expenses" not in df.columns:
        return {}

    df = df.copy()

    # Clean numeric column
    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce").fillna(0)

    # Optional month filtering
    if month and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df[df["date"].dt.strftime("%Y-%m") == month]

    return (
        df.groupby("category")["expenses"]
        .sum()
        .round(2)
        .to_dict()
    )


# =====================================================
# Budget Comparison Engine
# =====================================================

def compare_to_budget(actual: Dict[str, float], budget: Dict[str, float]) -> Dict:
    comparison = {}

    for category, limit in budget.items():
        spent = actual.get(category, 0.0)
        remaining = limit - spent
        progress = spent / limit if limit > 0 else 0.0

        status = "Healthy"
        if progress >= 1.0:
            status = "Over Budget"
        elif progress >= 0.85:
            status = "Warning"

        comparison[category] = {
            "spent": round(spent, 2),
            "limit": round(limit, 2),
            "remaining": round(remaining, 2),
            "progress": round(progress, 3),
            "status": status
        }

    return comparison


# =====================================================
# Budget Health Summary
# =====================================================

def budget_health_score(comparison: Dict) -> Dict:
    """
    Returns overall budget performance score (0–100)
    """

    if not comparison:
        return {
            "score": 100,
            "over_budget_categories": 0,
            "warning_categories": 0
        }

    total_categories = len(comparison)
    over_budget = 0
    warning = 0

    for cat_data in comparison.values():
        if cat_data["status"] == "Over Budget":
            over_budget += 1
        elif cat_data["status"] == "Warning":
            warning += 1

    # Weighted scoring
    penalty = (over_budget * 15) + (warning * 5)
    score = max(0, 100 - penalty)

    return {
        "score": score,
        "over_budget_categories": over_budget,
        "warning_categories": warning
    }