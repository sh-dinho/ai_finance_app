# modules/pipeline.py

from typing import Dict, Any
from .models import FinancialDataBundle, FISReport
from .validation import validate_bundle
from .fis import generate_fis_report_from_bundle
from .recommendations import generate_recommendations


def run_fis_pipeline(bundle: FinancialDataBundle) -> Dict[str, Any]:
    """
    Fully automated pipeline:
    - Validates inputs
    - Runs the full Financial Intelligence System
    - Generates recommendations
    - Returns a structured response for Streamlit
    """

    # 1. Validate all inputs
    validate_bundle(bundle)

    # 2. Run the full FIS
    fis_report: FISReport = generate_fis_report_from_bundle(bundle)

    # 3. Convert dataclass to dict
    fis_dict = {
        "ratios": fis_report.ratios,
        "emergency_fund": fis_report.emergency_fund,
        "income_insights": fis_report.income_insights,
        "trend_insights": fis_report.trend_insights,
        "forecast": fis_report.forecast,
        "discipline_risk": fis_report.discipline_risk,
        "habits": fis_report.habits,
        "goals": fis_report.goals,
        "goal_insights": fis_report.goal_insights,
        "intelligence_score": fis_report.intelligence_score
    }

    # 4. Generate recommendations
    recommendations = generate_recommendations(fis_dict)

    # 5. Return combined output
    return {
        "fis_report": fis_dict,
        "recommendations": recommendations
    }