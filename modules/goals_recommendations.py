# modules/goals_recommendations.py

from datetime import date
from typing import Dict, Any, Optional
import math


def forecast_goal_completion(
    current_value: float,
    target_value: float,
    daily_savings_rate: float,
    target_date: Optional[date]
) -> Dict[str, Any]:
    if target_value <= 0:
        return {
            "projected_completion_date": None,
            "will_meet_deadline": None,
            "days_ahead_or_behind": None
        }

    remaining = max(target_value - current_value, 0)

    if daily_savings_rate <= 0:
        return {
            "projected_completion_date": None,
            "will_meet_deadline": False if target_date else None,
            "days_ahead_or_behind": None
        }

    days_needed = math.ceil(remaining / daily_savings_rate)
    projected_completion = date.today().fromordinal(date.today().toordinal() + days_needed)

    if not target_date:
        return {
            "projected_completion_date": projected_completion,
            "will_meet_deadline": None,
            "days_ahead_or_behind": None
        }

    days_remaining = (target_date - date.today()).days
    will_meet = days_needed <= days_remaining
    days_diff = days_remaining - days_needed

    return {
        "projected_completion_date": projected_completion,
        "will_meet_deadline": will_meet,
        "days_ahead_or_behind": days_diff
    }


def goal_recommendation(
    goal_name: str,
    goal_data: Dict[str, Any],
    current_value: float,
    monthly_savings: float
) -> Dict[str, Any]:
    target = goal_data.get("target", 0)
    target_date: Optional[date] = goal_data.get("target_date")

    if target <= 0:
        return {
            "goal_name": goal_name,
            "required_daily": None,
            "required_monthly": None,
            "recommendation": "Invalid goal target."
        }

    remaining = max(target - current_value, 0)

    if not target_date:
        return {
            "goal_name": goal_name,
            "required_daily": None,
            "required_monthly": None,
            "recommendation": "No deadline set — increase savings to reach the goal sooner."
        }

    days_remaining = max((target_date - date.today()).days, 0)

    if days_remaining == 0:
        return {
            "goal_name": goal_name,
            "required_daily": None,
            "required_monthly": None,
            "recommendation": "Deadline reached — goal is now overdue."
        }

    required_daily = remaining / days_remaining
    required_monthly = required_daily * 30

    if monthly_savings >= required_monthly:
        rec = "You are on track — maintain your current savings rate."
    else:
        increase = required_monthly - monthly_savings
        rec = f"Increase monthly savings by ${increase:.2f} to stay on track."

    return {
        "goal_name": goal_name,
        "required_daily": round(required_daily, 2),
        "required_monthly": round(required_monthly, 2),
        "recommendation": rec
    }


def generate_goal_insights(
    goals: Dict[str, Dict[str, Any]],
    current_values: Dict[str, float],
    monthly_savings: float
) -> Dict[str, Dict[str, Any]]:
    insights: Dict[str, Dict[str, Any]] = {}

    daily_rate = monthly_savings / 30 if monthly_savings > 0 else 0

    for name, g in goals.items():
        current = current_values.get(name, 0.0)

        forecast = forecast_goal_completion(
            current_value=current,
            target_value=g["target"],
            daily_savings_rate=daily_rate,
            target_date=g.get("target_date")
        )

        rec = goal_recommendation(
            goal_name=name,
            goal_data=g,
            current_value=current,
            monthly_savings=monthly_savings
        )

        insights[name] = {
            "forecast": forecast,
            "recommendation": rec
        }

    return insights