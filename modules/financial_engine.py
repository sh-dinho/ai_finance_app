"""
financial_engine.py

Core financial intelligence engine:
- Ratios & metrics
- Emergency fund status
- Net worth projection
- FIRE number
- Stress index
- Risk profile
- Goal progress
- Composite financial intelligence score
"""

from typing import List, Dict, Any, Optional
from .core import FinancialSnapshot


class FinancialEngine:

    # ==============================
    # 1️⃣ Ratios & Metrics
    # ==============================
    @staticmethod
    def calculate_ratios(snapshot: FinancialSnapshot) -> Dict[str, float]:
        """
        Compute core financial ratios from a snapshot.
        """

        # Debt-to-income: only meaningful if high-interest debt exists
        debt_to_income = (
            snapshot.liquid_assets_to_debt or 0
            if snapshot.has_high_interest_debt
            else 0
        )

        # Expense ratio: expenses / income
        expense_ratio = (
            snapshot.monthly_expenses / snapshot.monthly_income
            if snapshot.monthly_income > 0
            else 1.0
        )

        # Savings ratio: already provided
        savings_ratio = snapshot.savings_rate

        # Debt-to-asset: liquidity vs net worth
        if snapshot.net_worth > 0 and snapshot.liquid_assets_to_debt is not None:
            debt_to_asset = snapshot.liquid_assets_to_debt / snapshot.net_worth
        else:
            debt_to_asset = 0.0

        return {
            "debt_to_income": round(debt_to_income, 3),
            "expense_ratio": round(expense_ratio, 3),
            "savings_ratio": round(savings_ratio, 3),
            "debt_to_asset": round(debt_to_asset, 3),
        }

    # ==============================
    # 2️⃣ Emergency Fund
    # ==============================
    @staticmethod
    def emergency_fund_status(snapshot: FinancialSnapshot) -> Dict[str, Any]:
        """
        Classify emergency fund strength based on months of coverage.
        """
        m = snapshot.emergency_months

        if m < 3:
            status = "High Risk"
        elif m < 6:
            status = "Moderate"
        else:
            status = "Strong"

        return {
            "coverage_months": round(m, 2),
            "status": status
        }

    # ==============================
    # 3️⃣ Net Worth Projection
    # ==============================
    @staticmethod
    def project_net_worth(
        snapshot: FinancialSnapshot,
        annual_savings: float,
        annual_return: float = 0.05,
        years: int = 10
    ) -> List[Dict[str, float]]:
        """
        Project net worth over time with constant annual savings and return.
        """
        projections: List[Dict[str, float]] = []
        net_worth = snapshot.net_worth

        for year in range(1, years + 1):
            net_worth = net_worth * (1 + annual_return) + annual_savings
            projections.append({
                "year": year,
                "projected_net_worth": round(net_worth, 2)
            })

        return projections

    # ==============================
    # 4️⃣ FIRE Number
    # ==============================
    @staticmethod
    def calculate_fire_number(
        snapshot: FinancialSnapshot,
        withdrawal_rate: float = 0.04
    ) -> float:
        """
        Calculate FIRE number: annual expenses / withdrawal rate.
        """
        annual_expenses = snapshot.monthly_expenses * 12
        if withdrawal_rate <= 0:
            return float("inf")
        return round(annual_expenses / withdrawal_rate, 2)

    # ==============================
    # 5️⃣ Stress Index (0–100)
    # ==============================
    @staticmethod
    def calculate_stress_index(
        snapshot: FinancialSnapshot,
        emergency_status: str
    ) -> int:
        """
        Higher score = more financial stress.
        """
        score = 50

        # Savings rate
        if snapshot.savings_rate < 0.1:
            score += 20
        elif snapshot.savings_rate < 0.2:
            score += 10

        # Liquidity vs debt
        if snapshot.liquid_assets_to_debt is not None:
            if snapshot.liquid_assets_to_debt < 0.5:
                score += 15
            elif snapshot.liquid_assets_to_debt < 1.0:
                score += 5

        # Emergency fund
        if emergency_status == "High Risk":
            score += 15
        elif emergency_status == "Moderate":
            score += 5

        return max(0, min(100, score))

    # ==============================
    # 6️⃣ Risk Profile
    # ==============================
    @staticmethod
    def risk_profile(snapshot: FinancialSnapshot, age: int) -> str:
        """
        Simple risk profile based on age and savings behavior.
        """
        if age < 35 and snapshot.savings_rate > 0.2:
            return "Aggressive"
        elif age < 50:
            return "Balanced"
        else:
            return "Conservative"

    # ==============================
    # 7️⃣ Goal Progress
    # ==============================
    @staticmethod
    def calculate_goal_progress(
        goals: Dict[str, Dict[str, Any]],
        snapshot: FinancialSnapshot
    ) -> Dict[str, Dict[str, float]]:
        """
        Compute progress toward each goal based on net worth.
        """
        results: Dict[str, Dict[str, float]] = {}

        for goal_name, goal_data in goals.items():
            target = goal_data.get("target", 0)
            progress = snapshot.net_worth / target if target > 0 else 1.0

            results[goal_name] = {
                "target": float(target),
                "progress_percent": round(min(progress * 100, 100), 2)
            }

        return results

    # ==============================
    # 8️⃣ Composite Financial Intelligence Score
    # ==============================
    @staticmethod
    def financial_intelligence_score(
        snapshot: FinancialSnapshot,
        age: int,
        goals: Dict[str, Dict[str, Any]],
        *,
        discipline_risk_fn=None,
        health_fns: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Composite score combining financial health, behavior risk, and trends.
        """

        # Lazy import if not injected
        if health_fns is None:
            from modules.financial_health import (
                cashflow_score,
                emergency_score,
                debt_health_score,
                investing_readiness_score,
                financial_health_score,
            )
        else:
            cashflow_score = health_fns["cashflow_score"]
            emergency_score = health_fns["emergency_score"]
            debt_health_score = health_fns["debt_health_score"]
            investing_readiness_score = health_fns["investing_readiness_score"]
            financial_health_score = health_fns["financial_health_score"]

        if discipline_risk_fn is None:
            from modules.discipline_risk import calculate_discipline_risk
            discipline_risk_fn = calculate_discipline_risk

        # Subscores
        cashflow = cashflow_score(snapshot.savings_rate)
        emergency = emergency_score(snapshot.emergency_months)
        debt = debt_health_score(snapshot.has_high_interest_debt, snapshot.liquid_assets_to_debt)
        investing = investing_readiness_score(snapshot.investments > 0, snapshot.emergency_months)
        savings_score = cashflow

        fin_health = financial_health_score(
            cashflow, savings_score, emergency, debt, investing
        )
        fin_health_score = fin_health["score"]

        # Emergency status
        emergency_status = FinancialEngine.emergency_fund_status(snapshot)["status"]

        # Discipline risk
        risk = discipline_risk_fn(entries=[], budget_comparison=None)
        risk_factor = {
            "Low": 1.0,
            "Moderate": 0.9,
            "High": 0.75,
            "Critical": 0.5
        }.get(risk.get("risk_level", "Moderate"), 0.9)

        # Trend modifier
        trend_modifier = 1.0
        for t in [snapshot.expense_trend, snapshot.income_trend, snapshot.income_stability]:
            if isinstance(t, float):
                if t < 0:
                    trend_modifier -= 0.05
                elif t > 1.0:
                    trend_modifier -= 0.05

        trend_modifier = max(0.5, trend_modifier)

        composite_score = round(fin_health_score * risk_factor * trend_modifier)

        if composite_score >= 80:
            status = "Excellent"
        elif composite_score >= 60:
            status = "Good"
        elif composite_score >= 40:
            status = "Fair"
        else:
            status = "Poor"

        return {
            "score": composite_score,
            "status": status,
            "financial_health_score": fin_health_score,
            "discipline_risk_level": risk.get("risk_level"),
            "trend_modifier": round(trend_modifier, 2),
            "emergency_status": emergency_status,
        }