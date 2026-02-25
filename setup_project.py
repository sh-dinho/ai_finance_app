import os
import json
from pathlib import Path

# =====================================================
# Helpers
# =====================================================

def make_dir(path: str):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"📁 Directory ensured: {path}")


def make_file(path: str, content: str = "", overwrite: bool = False):
    """
    Create a file safely.
    - Will not overwrite unless overwrite=True
    """
    file_path = Path(path)

    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists() and not overwrite:
        print(f"⏩ Skipped existing file: {path}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📝 File written: {path}")


def write_json(path: str, content: dict, overwrite: bool = False):
    """Safely write JSON with indentation."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists() and not overwrite:
        print(f"⏩ Skipped existing JSON: {path}")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4)

    print(f"📦 JSON populated: {path}")


# =====================================================
# Project Structure
# =====================================================

project_structure = {
    "streamlit_app": [
        "Home.py",
        "Data_Entry.py",
        "Spending_Budget.py",
        "Goals.py",
        "Insights.py",
        "ui_simple.py"
    ],
    "modules": [
        "core.py",
        "category_detector.py",
        "budget.py",
        "forecasting.py",
        "habits.py",
        "goals.py",
        "trend_insights.py",
        "income_insights.py",
        "fis.py",
        "stress_and_projection.py"
    ],
    "data": [
        "user_inputs.json",
        "monthly_log.csv",
        "budgets.json",
        "categories.json",
        "goals.json"
    ],
    ".streamlit": [
        "config.toml"
    ]
}

root_files = [
    "requirements.txt",
    "README.md",
    ".gitignore"
]

# =====================================================
# Create Folders
# =====================================================

print("\n🚀 Setting up AI Finance App structure...\n")

for folder in project_structure.keys():
    make_dir(folder)

# =====================================================
# Create Files
# =====================================================

for folder, files in project_structure.items():
    for file in files:
        make_file(os.path.join(folder, file))

for file in root_files:
    make_file(file)

# =====================================================
# Default JSON Data
# =====================================================

json_data = {
    "data/user_inputs.json": {
        "age": 30,
        "employment_income": 0,
        "other_income": 0,
        "annual_expenses": 0,
        "emergency_fund": 0,
        "financial_assets": {
            "cash": 0,
            "chequing": 0,
            "savings": 0,
            "stocks": 0,
            "crypto": 0,
            "bonds": 0
        },
        "physical_assets": {
            "car": 0,
            "home": 0
        },
        "liabilities": {
            "credit_card": {"amount": 0, "rate": 0.19},
            "loan": {"amount": 0, "rate": 0.05}
        }
    },
    "data/budgets.json": {
        "Housing": 1800,
        "Utilities": 250,
        "Groceries": 600,
        "Transportation": 200,
        "Dining": 250,
        "Shopping": 300,
        "Health": 150,
        "Entertainment": 150,
        "Other": 200
    },
    "data/categories.json": {
        "Housing": ["rent", "mortgage", "property tax", "condo fee"],
        "Utilities": ["hydro", "electricity", "water", "internet", "wifi", "gas"],
        "Groceries": ["grocery", "superstore", "loblaws", "food", "market"],
        "Transportation": ["uber", "lyft", "gasoline", "fuel", "bus", "train"],
        "Dining": ["restaurant", "coffee", "cafe", "starbucks", "tim hortons"],
        "Shopping": ["amazon", "clothes", "electronics", "walmart"],
        "Health": ["pharmacy", "drug", "clinic", "dentist"],
        "Entertainment": ["netflix", "spotify", "movie", "game"],
        "Other": []
    },
    "data/goals.json": {
        "Emergency Fund": {"target": 15000, "target_date": "2027-01-01"},
        "Savings Goal": {"target": 20000, "target_date": "2026-12-31"},
        "Investment Goal": {"target": 50000, "target_date": "2030-01-01"},
        "Net Worth Goal": {"target": 100000, "target_date": "2028-01-01"},
        "Debt Payoff Goal": {"target": 0, "target_date": "2027-06-01"}
    }
}

for path, content in json_data.items():
    write_json(path, content)

# =====================================================
# config.toml
# =====================================================

make_file(
    ".streamlit/config.toml",
    """
[theme]
primaryColor="#4CAF50"
backgroundColor="#F7F9FB"
secondaryBackgroundColor="#FFFFFF"
textColor="#1A1A1A"
font="sans serif"
""",
    overwrite=True
)

# =====================================================
# requirements.txt
# =====================================================

make_file(
    "requirements.txt",
    """
streamlit
pandas
numpy
python-dateutil
""",
    overwrite=True
)

# =====================================================
# .gitignore
# =====================================================

make_file(
    ".gitignore",
    """
venv/
__pycache__/
*.pyc
.streamlit/
.env
""",
    overwrite=True
)

# =====================================================
# README.md
# =====================================================

make_file(
    "README.md",
    """
# AI Finance App

A beginner-friendly, AI-powered personal finance dashboard built with Streamlit.

## Features
- Daily or monthly data entry
- Automatic expense categorization
- Budget tracking
- Financial goals
- Stress index
- Health score
- Forecasting
- Habit tracking
- Multi-page dashboard

## Setup

1. Create a virtual environment:

   python -m venv venv

2. Activate it:

   Windows:
   venv\\Scripts\\activate

   Mac/Linux:
   source venv/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the app:

   streamlit run streamlit_app/Home.py
""",
    overwrite=True
)

print("\n✅ AI Finance App structure is ready.\n")