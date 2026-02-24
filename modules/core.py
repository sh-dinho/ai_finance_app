import math
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

# =====================================================
# Financial Intelligence Engine
# =====================================================

class FinancialEngine:

    # -----------------------------
    # Advanced Ratios
    # -----------------------------
    @staticmethod
    def calculate_ratios(metrics: Dict) -> Dict:
        income = metrics["total_income"]
        expenses = metrics["annual_expenses"]
        liabilities = metrics["total_liabilities"]
        assets = metrics["total_assets"]

        debt_to_income = liabilities / income if income else 0
        expense_ratio = expenses / income if income else 0
        savings_ratio = metrics["savings_rate"]
        debt_to_asset = liabilities / assets if assets else 0

        return {
            "debt_to_income": round(debt_to_income, 3),
            "expense_ratio": round(expense_ratio, 3),
            "savings_ratio": round(savings_ratio, 3),
            "debt_to_asset": round(debt_to_asset, 3),
        }

    # -----------------------------
    # Emergency Fund Health
    # -----------------------------
    @staticmethod
    def emergency_fund_coverage(user, metrics: Dict) -> Dict:
        monthly_expenses = metrics["monthly_expenses"]
        coverage_months = (
            user.emergency_fund / monthly_expenses
            if monthly_expenses > 0 else 0
        )

        status = "Strong"
        if coverage_months < 3:
            status = "High Risk"
        elif coverage_months < 6:
            status = "Moderate"

        return {
            "coverage_months": round(coverage_months, 2),
            "status": status
        }

    # -----------------------------
    # FIRE Number
    # -----------------------------
    @staticmethod
    def calculate_fire_number(annual_expenses: float, withdrawal_rate: float = 0.04) -> float:
        return round(annual_expenses / withdrawal_rate, 2)

    # -----------------------------
    # Net Worth Projection
    # -----------------------------
    @staticmethod
    def project_net_worth(
        current_net_worth: float,
        annual_savings: float,
        annual_return: float = 0.05,
        years: int = 10
    ) -> List[Dict]:

        projections = []
        net_worth = current_net_worth

        for year in range(1, years + 1):
            net_worth = net_worth * (1 + annual_return) + annual_savings
            projections.append({
                "year": year,
                "projected_net_worth": round(net_worth, 2)
            })

        return projections

    # -----------------------------
    # Financial Stress Index (0–100)
    # -----------------------------
    @staticmethod
    def calculate_stress_index(metrics: Dict, emergency_status: str) -> int:
        score = 50

        if metrics["savings_rate"] < 0.1:
            score += 20

        if metrics["total_liabilities"] > metrics["total_income"]:
            score += 15

        if emergency_status == "High Risk":
            score += 15
        elif emergency_status == "Moderate":
            score += 5

        score = max(0, min(100, score))
        return score

    # -----------------------------
    # Goal Progress
    # -----------------------------
    @staticmethod
    def calculate_goal_progress(goals: Dict, current_net_worth: float) -> Dict:
        results = {}

        for goal_name, goal_data in goals.items():
            target = goal_data["target"]
            progress = (current_net_worth / target) if target > 0 else 1

            results[goal_name] = {
                "target": target,
                "progress_percent": round(min(progress * 100, 100), 2)
            }

        return results

    # -----------------------------
    # Risk Profile Score
    # -----------------------------
    @staticmethod
    def risk_profile(age: int, savings_rate: float) -> str:
        if age < 35 and savings_rate > 0.2:
            return "Aggressive"
        elif age < 50:
            return "Balanced"
        else:
            return "Conservative"

    # -----------------------------
    # Retirement Projection
    # -----------------------------
    @staticmethod
    def retirement_projection(
        current_age: int,
        retirement_age: int,
        current_net_worth: float,
        annual_savings: float,
        annual_return: float = 0.05
    ) -> float:

        years = retirement_age - current_age
        if years <= 0:
            return current_net_worth

        net_worth = current_net_worth
        for _ in range(years):
            net_worth = net_worth * (1 + annual_return) + annual_savings

        return round(net_worth, 2)