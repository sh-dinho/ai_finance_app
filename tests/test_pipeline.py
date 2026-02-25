from modules.pipeline import run_fis_pipeline


def test_pipeline_execution(mock_bundle):
    # The fixture is automatically injected
    result = run_fis_pipeline(mock_bundle)

    assert "fis_report" in result
    assert result["fis_report"]["intelligence_score"]["score"] > 0
    assert result["fis_report"]["intelligence_score"]["status"] in ["Excellent", "Good", "Fair", "Poor"]
