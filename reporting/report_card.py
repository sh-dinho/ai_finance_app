from reporting.utils import (
    grade_from_score,
    status_narrative,
    habits_narrative,
    goals_narrative,
)
from reporting.formatters import header, section, line


def generate_report_card(results, settings) -> str:
    intel = results["intelligence_report"]
    insights = results["insights"]

    score = intel["score"]
    status = intel["status"]
    grade = grade_from_score(score, settings.thresholds)

    habits_status = insights["habits"].get("status", "Unknown")
    goal_health = insights["goals"].get("goal_health_score", 0)
    goals = insights["goals"].get("per_goal", {})

    narrative = " ".join([
        status_narrative(status),
        habits_narrative(habits_status),
        goals_narrative(goal_health, settings.thresholds),
    ])

    lines = []

    # Header
    lines.append(header("Financial Report Card"))
    lines.append(line(f"Overall Grade: {grade} ({score}/100)"))
    lines.append(line(f"Status: {status}"))

    # Summary
    lines.append(section("Summary"))
    lines.append(line(narrative))

    # Key Metrics
    lines.append(section("Key Metrics"))
    lines.append(line(f"Income Reliability: {insights['income'].get('reliability_score', 'N/A')}%"))
    lines.append(line(f"Habit Strength: {habits_status}"))
    lines.append(line(f"Goal Health Score: {goal_health}/100"))

    # Goal Progress
    lines.append(section("Goal Progress"))
    for name, data in goals.items():
        progress = data.get("progress_pct", 0)
        g_status = data.get("status", "Unknown")
        req_monthly = data.get("required_monthly", None)
        rec = data.get("recommendation", "")

        goal_line = f"- {name}: {progress}% complete ({g_status})"
        if req_monthly is not None:
            goal_line += f" | Required Monthly: ${req_monthly}"
        if rec:
            goal_line += f" | {rec}"

        lines.append(line(goal_line))

    return "\n".join(lines)
