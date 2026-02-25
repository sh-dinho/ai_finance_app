# modules/report_card.py
from typing import Dict, Any


def grade_from_score(score: int) -> str:
    """Converts a numeric 0-100 score into a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def build_financial_report_card(fis: Dict[str, Any]) -> Dict[str, Any]:
    score = fis["score"]
    # This is where the reference was likely failing
    grade = grade_from_score(score)

    sub = {
        "Financial Health": fis["financial_health_score"],
        "Income Factor": int(fis.get("income_factor", 0) * 100),
        # ... rest of your subscores
    }

    return {
        "grade": grade,
        "score": score,
        "status": fis["status"],
        "subscores": sub,
        "discipline_risk_level": fis["discipline_risk_level"],
    }


def summarize_financial_life(
        fis: Dict[str, Any],
        discipline_risk: Dict[str, Any],
        income_insights: Dict[str, Any],
        emergency_fund: Dict[str, Any],
        goals: Dict[str, Any],
) -> str:
    """Combines various insights into a readable summary paragraph."""
    parts = []

    # Example logic
    score = fis.get('score', 0)
    parts.append(f"Your FIS Score is {score} ({grade_from_score(score)}).")

    risk = discipline_risk.get('risk_level', 'Unknown')
    parts.append(f"Your discipline risk is {risk.lower()}.")

    return " ".join(parts)