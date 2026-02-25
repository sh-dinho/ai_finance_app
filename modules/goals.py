from dataclasses import dataclass
from datetime import date
from typing import Dict, Any, List
import math


@dataclass
class Goal:
    name: str
    target: float
    target_date: date


def analyze_goals(goals: Dict[str, Goal], current_values: Dict[str, float], monthly_savings: float) -> Dict[str, Any]:
    insights = {}
    total_needed = 0

    for name, goal in goals.items():
        current = current_values.get(name, 0)
        remaining = max(0, goal.target - current)
        months_left = ((goal.target_date - date.today()).days) / 30.44

        required_monthly = remaining / months_left if months_left > 0 else remaining
        status = "On Track" if monthly_savings >= required_monthly else "Behind"

        insights[name] = {
            "progress_pct": round((current / goal.target) * 100, 1),
            "status": status,
            "required_monthly": round(required_monthly, 2),
            "recommendation": "Maintain pace" if status == "On Track" else f"Increase savings by ${round(required_monthly - monthly_savings, 2)}"
        }
    return insights