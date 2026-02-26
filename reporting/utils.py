def grade_from_score(score: float, thresholds):
    if score >= thresholds.grading.A:
        return "A"
    if score >= thresholds.grading.B:
        return "B"
    if score >= thresholds.grading.C:
        return "C"
    return "F"


def status_narrative(status: str):
    if status == "Excellent":
        return "Your financial position is strong and improving."
    if status == "Good":
        return "Your financial position is solid with room for optimization."
    if status == "Fair":
        return "Your financial position is stable but needs attention."
    return "Your financial position requires focused improvement."


def habits_narrative(habit_status: str):
    if habit_status == "Excellent":
        return "Your financial habits are consistent and reliable."
    if habit_status == "Moderate":
        return "Your habits are stable but could be more consistent."
    return "Your habits show volatility that may be affecting progress."


def goals_narrative(goal_health: float, thresholds):
    if goal_health >= thresholds.goals.on_track:
        return "You are on track with most of your goals."
    if goal_health >= thresholds.goals.behind:
        return "Some goals are behind schedule but still recoverable."
    return "Several goals are significantly behind; consider adjusting savings or timelines."
