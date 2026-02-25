# modules/pipeline.py

from typing import Dict, Any, Optional
from dataclasses import asdict
import logging

from .models import FinancialDataBundle, FISReport, FISPipelineOutput
from .validation import validate_bundle
from .fis import generate_fis_report_from_bundle
from .recommendations import generate_recommendations

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error (optional — replace with your own if needed)."""
    pass


def run_fis_pipeline(
    bundle: FinancialDataBundle,
    include_recommendations: bool = True,
    return_dict: bool = True
) -> Dict[str, Any] | FISPipelineOutput:
    """
    Fully automated pipeline:
    - Validates inputs
    - Runs the full Financial Intelligence System
    - Optionally generates recommendations
    - Returns either a dict (for Streamlit) or a dataclass (for typed usage)
    """

    logger.info("Starting FIS pipeline")

    try:
        # 1. Validate all inputs
        logger.debug("Validating FinancialDataBundle")
        validate_bundle(bundle)
        logger.debug("Validation successful")

        # 2. Run the full FIS
        logger.debug("Generating FIS report from bundle")
        fis_report: FISReport = generate_fis_report_from_bundle(bundle)
        logger.debug("FIS report generated")

        # 3. Convert dataclass to dict (for UI / JSON)
        fis_dict = asdict(fis_report)
        logger.debug("Converted FISReport to dict")

        # 4. Optionally generate recommendations
        recommendations: Optional[Dict[str, Any]] = None
        if include_recommendations:
            logger.debug("Generating recommendations")
            recommendations = generate_recommendations(fis_dict)
            logger.debug("Recommendations generated")

        # 5. Build structured output dataclass
        pipeline_output = FISPipelineOutput(
            fis_report=fis_report,
            recommendations=recommendations or {}
        )

        logger.info("FIS pipeline completed successfully")

        # 6. Return either dict (for Streamlit) or dataclass (for typed use)
        if return_dict:
            return {
                "fis_report": fis_dict,
                "recommendations": recommendations or {}
            }

        return pipeline_output

    except ValidationError as e:
        logger.warning("Validation error in FIS pipeline: %s", e)
        if return_dict:
            return {
                "error": "Validation error",
                "details": str(e)
            }
        raise

    except Exception as e:
        logger.exception("Unexpected error in FIS pipeline")
        if return_dict:
            return {
                "error": "Unexpected error occurred while running the FIS pipeline",
                "details": str(e)
            }
        raise