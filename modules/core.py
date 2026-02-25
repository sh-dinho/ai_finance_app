from dataclasses import dataclass, field
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

@dataclass
class MonthlyLogEntry:
    month_index: int
    income: float
    expenses: float
    savings: float
    notes: Optional[str] = None

@dataclass
class FinancialSnapshot:
    """Represents the user's current state. Ratios are auto-calculated."""
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    emergency_months: float
    investments: float
    has_high_interest_debt: bool
    liquid_assets_to_debt: float
    income_stability: float  # 0.0 to 1.0
    income_trend: float      # e.g., 1.05 for +5%
    expense_trend: float     # e.g., 0.95 for -5%

    @property
    def expense_ratio(self) -> float:
        return self.monthly_expenses / self.monthly_income if self.monthly_income > 0 else 1.0

    @property
    def is_investing(self) -> bool:
        return self.investments > 0