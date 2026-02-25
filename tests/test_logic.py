from modules.report_card import grade_from_score, build_financial_report_card

def test_grade_calculation():
    assert grade_from_score(95) == "A"
    assert grade_from_score(75) == "C"
    assert grade_from_score(40) == "F"

def test_report_card_structure():
    mock_fis = {
        "score": 85,
        "status": "Good",
        "financial_health_score": 80,
        "income_factor": 0.9,
        "trend_factor": 0.8,
        "habit_factor": 0.7,
        "forecast_factor": 0.6,
        "goal_factor": 0.5,
        "discipline_risk_level": "Low"
    }
    report = build_financial_report_card(mock_fis)
    assert report["grade"] == "B"
    assert "subscores" in report
    assert report["subscores"]["Income Factor"] == 90