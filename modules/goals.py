import json
from datetime import date, datetime
from typing import Dict, Any, Optional


# =====================================================
# Load Goals
# =====================================================

def load_goals(path: str = "data/goals.json") -> Dict[str, Dict[str, Any]]:
    """
    Load user goals from JSON.

    Expected format:
    {
        "Emergency Fund": {"target": 15000, "target_date": "2027-01-01"},
        ...
    }

    Returns:
        {
            "Emergency Fund": {
                "target": float,
                "target_date": date | None
            },
            ...
        }
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    goals: Dict[str, Dict[str, Any]] = {}

    for name, g in raw.items():
        try:
            target_value = float(g["target"])
            target_date = (
                date.fromisoformat(g["target_date"])
                if "target_date" in g and g["target_date"]
                else None
            )
        except Exception:
            # Skip malformed entries
            continue

        goals[name] = {
            "target": target_value,
            "target_date": target_date
        }

    return goals


# =====================================================
# Single Goal Progress
# =====================================================

def calculate_goal_progress(
    goal_name: str,
    goal_data: Dict[str, Any],
    current_value: float
) -> Dict[str, Any]:
    """
    Calculate progress toward a single goal.

    Returns:
        {
            "goal_name": str,
            "current_value": float,
            "target": float,
            "progress": float (0–1),
            "days_remaining": int | None,
            "status": str,
            "daily_required": float | None,
            "pace_required_pct": float | None
        }
    """

    target = goal_data.get("target", 0.0)
    target_date: Optional[date] = goal_data.get("target_date")

    today = date.today()

    # Progress ratio
    progress = current_value / target if target > 0 else 0
    progress = min(progress, 1.0)

    # Days remaining (None if no date)
    if target_date:
        days_remaining = max((target_date - today).days, 0)
    else:
        days_remaining = None

    # Determine status
    if progress >= 1.0:
        status = "Completed"
    elif target_date is None:
        status = "Active"
    elif days_remaining == 0:
        status = "Overdue"
    elif progress >= 0.9:
        status = "Ahead of Schedule"
    elif progress >= 0.75:
        status = "On Track"
    else:
        status = "At Risk"

    # Additional metrics
    daily_required = None
    pace_required_pct = None

    if target_date and target > 0 and progress < 1.0:
        remaining = target - current_value
        if days_remaining > 0:
            daily_required = round(remaining / days_remaining, 2)
            pace_required_pct = round((remaining / target) * 100, 2)

    return {
        "goal_name": goal_name,
        "current_value": round(current_value, 2),
        "target": target,
        "progress": round(progress, 3),
        "days_remaining": days_remaining,
        "status": status,
        "daily_required": daily_required,
        "pace_required_pct": pace_required_pct
    }


# =====================================================
# Batch Goal Progress
# =====================================================

def calculate_all_goals_progress(
    goals: Dict[str, Dict[str, Any]],
    current_values: Dict[str, float]
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate progress for all goals.

    `current_values` should map goal names → current numeric value.
    """
    results: Dict[str, Dict[str, Any]] = {}

    for name, g in goals.items():
        current = current_values.get(name, 0.0)
        results[name] = calculate_goal_progress(name, g, current)

    return results