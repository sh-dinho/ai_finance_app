import os
from datetime import datetime

from config.settings import Settings
from data.data_loader import load_csv, load_json
from data.bundle_builder import build_bundle
from scripts.email_sender import send_report_email
from app import run_full_fis


def main():
    settings = Settings.load()

    # Load data paths from config
    monthly_path = settings.paths.data.monthly_entries
    daily_path = settings.paths.data.daily_logs

    df_monthly = load_csv(monthly_path)
    df_daily = load_csv(daily_path)

    # Optional JSON files for goals + current values
    raw_goals = load_json("data/goals.json")
    current_values = load_json("data/current_values.json")

    bundle = build_bundle(settings, df_monthly, df_daily, raw_goals, current_values)

    report = run_full_fis(bundle)

    # Save report
    output_dir = settings.paths.output.reports_folder
    os.makedirs(output_dir, exist_ok=True)

    filename = f"fis_report_{datetime.now().strftime('%Y-%m-%d')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(report)

    print(f"[report] Saved: {filepath}")

    # Email report
    send_report_email(settings, report)


if __name__ == "__main__":
    main()
