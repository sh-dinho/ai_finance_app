import os
import shutil
import subprocess
import sys

PROJECT_ROOT = "financial_intelligence_system"


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def clean_project():
    if os.path.exists(PROJECT_ROOT):
        print(f"Deleting existing project folder: {PROJECT_ROOT}")
        shutil.rmtree(PROJECT_ROOT)
    os.makedirs(PROJECT_ROOT)
    print(f"Created clean project folder: {PROJECT_ROOT}")


def create_structure():
    folders = [
        "core",
        "scoring",
        "pipeline",
        "reporting",
        "data",
        "scripts",
        "config",
    ]

    for folder in folders:
        os.makedirs(os.path.join(PROJECT_ROOT, folder), exist_ok=True)


def create_files():
    write(f"{PROJECT_ROOT}/core/models.py", """# models.py
# (Paste your full models code here)
""")

    write(f"{PROJECT_ROOT}/core/snapshot.py", """# snapshot.py
# (Paste your full FinancialSnapshot implementation here)
""")

    write(f"{PROJECT_ROOT}/scoring/health.py", """# health scoring engine
""")

    write(f"{PROJECT_ROOT}/scoring/habits.py", """# habit scoring engine
""")

    write(f"{PROJECT_ROOT}/scoring/goals.py", """# goal scoring engine
""")

    write(f"{PROJECT_ROOT}/scoring/composite.py", """# composite scoring engine
""")

    write(f"{PROJECT_ROOT}/pipeline/fis_report.py", """from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class FISReport:
    intelligence: Dict[str, Any]
    insights: Dict[str, Any]
""")

    write(f"{PROJECT_ROOT}/pipeline/pipeline.py", """# FISPipeline orchestrator
""")

    write(f"{PROJECT_ROOT}/reporting/report_card.py", """# generate_report_card implementation
""")

    write(f"{PROJECT_ROOT}/data/data_loader.py", """# data loader implementation
""")

    write(f"{PROJECT_ROOT}/scripts/email_sender.py", """# email sender implementation
""")

    write(f"{PROJECT_ROOT}/scripts/run_local.py", """# automated runner script
""")

    write(f"{PROJECT_ROOT}/app.py", """from pipeline.pipeline import FISPipeline
from reporting.report_card import generate_report_card

def run_full_fis(bundle):
    pipeline = FISPipeline()
    results = pipeline.run(bundle)
    return generate_report_card({
        "intelligence_report": results.intelligence,
        "insights": results.insights
    })
""")

    write(f"{PROJECT_ROOT}/config/weights.yaml", """health:
  weights:
    cashflow: 0.25
    emergency: 0.25
    debt: 0.25
    investing: 0.25
""")

    write(f"{PROJECT_ROOT}/requirements.txt", """pandas
numpy
""")

    print("All files created successfully.")


def create_virtual_env():
    print("Creating virtual environment...")
    venv_path = os.path.join(PROJECT_ROOT, "venv")

    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    print(f"Virtual environment created at: {venv_path}")

    pip_path = os.path.join(venv_path, "bin", "pip") if os.name != "nt" else os.path.join(venv_path, "../scripts", "pip.exe")

    print("Installing dependencies...")
    subprocess.run([pip_path, "install", "-r", f"{PROJECT_ROOT}/requirements.txt"], check=True)
    print("Dependencies installed.")


if __name__ == "__main__":
    clean_project()
    create_structure()
    create_files()
    create_virtual_env()
    print("Project setup complete!")
