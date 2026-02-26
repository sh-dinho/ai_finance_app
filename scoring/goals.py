from scoring.utils import clamp, pct


def analyze_goals(goals, current_values, monthly_savings):
    per_goal = {}
    total_score = 0
    count = 0

    for name, goal in goals.items():
        current = current_values.get(name, 0.0)
        progress = pct(current, goal.target)
        status = (
            "On Track" if progress >= 80
            else "Behind" if progress >= 50
            else "Off Track"
        )

        required_monthly = max((goal.target - current) / max((goal.target_date.year - 2026) * 12, 1), 0)

        per_goal[name] = {
            "progress_pct": clamp(progress),
            "status": status,
            "required_monthly": required_monthly,
            "recommendation": "Increase monthly savings" if required_monthly > monthly_savings else "On pace",
        }

        total_score += clamp(progress)
        count += 1

    goal_health_score = clamp(total_score / count) if count else 0

    return {
        "per_goal": per_goal,
        "goal_health_score": goal_health_score,
    }
