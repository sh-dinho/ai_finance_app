from dataclasses import dataclass
from typing import Optional


# =====================================================
# Monthly Log Entry (Used by trend, stability, habits)
# =====================================================

@dataclass
class MonthlyLogEntry:
    """
    Represents a single month of financial activity.
    Used by income trend, stability, habit streaks, etc.
    """
    month_index: int
    income: float
    expenses: float
    savings: float
    notes: Optional[str] = None


# =====================================================
# Financial Snapshot (Used by FinancialEngine)
# =====================================================

@dataclass
class FinancialSnapshot:
    """
    Represents a snapshot of a user's financial situation.
    Used across all financial intelligence modules.
    """
    savings_rate: float
    emergency_months: float
    has_high_interest_debt: bool
    liquid_assets_to_debt: Optional[float]
    expense_trend: float | str
    income_stability: float | str
    income_trend: float | str
    monthly_expenses: float
    monthly_income: float
    emergency_fund: float
    liquid_assets: float
    investments: float
    net_worth: float