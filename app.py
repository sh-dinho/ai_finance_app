from config.settings import Settings
from pipeline.pipeline import FISPipeline
from reporting.report_card import generate_report_card

settings = Settings.load()

def run_full_fis(bundle):
    pipeline = FISPipeline(settings)
    results = pipeline.run(bundle)
    return generate_report_card({
        "intelligence_report": results.intelligence,
        "insights": results.insights
    }, settings)
