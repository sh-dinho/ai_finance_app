from typing import Dict, Any, List
from .core import FinancialSnapshot

class FinancialEngine:
    @staticmethod
    def calculate_ratios(snapshot: FinancialSnapshot) -> Dict[str, float]:
        """Compute core financial ratios."""
        return {
            "savings_rate": snapshot.savings_rate,
            "expense_ratio": snapshot.expense_ratio,
            "debt_to_income": snapshot.liquid_assets_to_debt if snapshot.has_high_interest_debt else 0.0
        }

    @staticmethod
    def project_net_worth(snapshot: FinancialSnapshot, years: int = 10, annual_return: float = 0.07) -> Dict[str, Any]:
        """Calculates future wealth based on current investments and savings."""
        monthly_rate = annual_return / 12
        months = years * 12
        monthly_savings = snapshot.monthly_income - snapshot.monthly_expenses
        
        current_nw = snapshot.investments
        for _ in range(months):
            current_nw = (current_nw * (1 + monthly_rate)) + monthly_savings
            
        return {
            "years": years,
            "projected_net_worth": round(current_nw, 2)
        }