import pprint
from colorama import Fore, Style, init

# Mock Data
from mock_data.generator import generate_mock_persona

# Updated Modules
from modules.models import FinancialDataBundle
from modules.pipeline import run_fis_pipeline
from modules.report_card import generate_report_card

init(autoreset=True)


def section(title: str):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {title.upper()} ==={Style.RESET_ALL}\n")


def run_persona_analysis(persona_name: str):
    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n🚀 Initializing Analysis for: {persona_name}{Style.RESET_ALL}")

    # 1. Generate full mock dataset
    # The generator now returns a dict containing all necessary components
    data = generate_mock_persona(persona_name, months=24)

    # 2. Wrap data into the standardized Bundle
    # This ensures type safety and validation before the pipeline runs
    bundle = FinancialDataBundle(
        snapshot=data["snapshot"],
        entries=data["entries"],
        df_daily=data["df_daily"],
        goals=data["goals"],
        current_goal_values=data["current_goal_values"],
        monthly_savings=data["monthly_savings"],
        age=data["age"]
    )

    # 3. Execute the Pipeline
    # This replaces the 50+ lines of manual module calls in your original script
    results = run_fis_pipeline(bundle)

    # ---------------------------------------------------------
    section("Intelligence Report")
    pprint.pprint(results["intelligence_report"])

    # ---------------------------------------------------------
    section("Detailed Insights")
    print(Fore.YELLOW + "Income Reliability:")
    pprint.pprint(results["insights"]["income"])

    print(Fore.YELLOW + "\nGoal Progress & Recommendations:")
    pprint.pprint(results["insights"]["goals"])

    # ---------------------------------------------------------
    section("Final Report Card")
    # This converts the raw data into the human-readable format
    print(Fore.WHITE + generate_report_card(results))

    print(f"\n{Fore.GREEN}{Style.BRIGHT}Analysis Complete ✔{Style.RESET_ALL}\n")


if __name__ == "__main__":
    # Test with the freelancer persona
    run_persona_analysis("freelancer")