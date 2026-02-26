from config.settings import Settings
from pipeline.pipeline import FISPipeline
from reporting.report_card import generate_report_card
from core.models import FinancialDataBundle

settings = Settings.load()

def run_full_fis(bundle):
    pipeline = FISPipeline(settings)
    results = pipeline.run(bundle)
    return generate_report_card({
        "intelligence_report": results.intelligence,
        "insights": results.insights
    }, settings)

def main():
    # TODO: build or load a real FinancialDataBundle
    bundle = FinancialDataBundle.load_from_source("data/sample.json")
    report = run_full_fis(bundle)
    print(report)

if __name__ == "__main__":
    main()