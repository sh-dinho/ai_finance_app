import json
from pathlib import Path
from typing import Dict, Any
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
    month: str = None,
    include_total: bool = True
) -> Dict[str, float]:
    """
    Optionally filter by month (YYYY-MM format).
    Requires 'date', 'category', and 'expenses' columns.
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

    category_totals = (
        df.groupby("category")["expenses"]
        .sum()
        .round(2)
        .to_dict()
    )

    if include_total:
        category_totals["_total_spent"] = round(df["expenses"].sum(), 2)

    return category_totals


# =====================================================
# Budget Comparison Engine
# =====================================================

def compare_to_budget(
    actual: Dict[str, float],
    budget: Dict[str, float]
) -> Dict[str, Dict[str, Any]]:
    """
    Compares actual spending to budget limits.
    Includes handling for categories not in the budget.
    """

    comparison = {}

    # First handle categories that exist in the budget
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

    # Handle categories NOT in the budget
    for category, spent in actual.items():
        if category not in budget and category != "_total_spent":
            comparison[category] = {
                "spent": round(spent, 2),
                "limit": 0.0,
                "remaining": -round(spent, 2),
                "progress": 1.0,
                "status": "Uncategorized"
            }

    # Sort by highest progress (overspending first)
    comparison = dict(
        sorted(comparison.items(), key=lambda x: x[1]["progress"], reverse=True)
    )

    return comparison


# =====================================================
# Budget Health Summary
# =====================================================

def budget_health_score(comparison: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returns overall budget performance score (0–100)
    with improved severity-based scoring.
    """

    if not comparison:
        return {
            "score": 100,
            "over_budget_categories": 0,
            "warning_categories": 0,
            "uncategorized": 0
        }

    over_budget = 0
    warning = 0
    uncategorized = 0
    severity_penalty = 0

    for cat_data in comparison.values():
        status = cat_data["status"]

        if status == "Over Budget":
            over_budget += 1

        elif status == "Warning":
            warning += 1

        elif status == "Uncategorized":
            uncategorized += 1

        # Severity penalty: overspending beyond 100%
        if cat_data["limit"] > 0:
            excess_ratio = max(0, cat_data["progress"] - 1.0)
            severity_penalty += excess_ratio * 20  # 20 points per 100% overspend

    # Base penalties
    base_penalty = (over_budget * 15) + (warning * 5) + (uncategorized * 3)

    score = max(0, 100 - base_penalty - severity_penalty)

    return {
        "score": round(score, 1),
        "over_budget_categories": over_budget,
        "warning_categories": warning,
        "uncategorized": uncategorized
    }