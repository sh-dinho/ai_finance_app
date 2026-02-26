from dataclasses import dataclass, field
from typing import List


@dataclass
class FinancialSnapshot:
    """
    Canonical, version-agnostic snapshot of a user's current financial state.
    """
    monthly_income: float
    monthly_expenses: float
    investments: float
    liquid_assets: float
    debt: float
    emergency_fund: float
    has_high_interest_debt: bool

    income_history: List[float] = field(default_factory=list)
    expense_history: List[float] = field(default_factory=list)

    # Derived metrics
    savings_amount: float = 0.0
    savings_rate: float = 0.0
    net_worth: float = 0.0
    expense_coverage_months: float = 0.0
    debt_to_income: float = 0.0

    def __post_init__(self):
        self._compute_derived()

    def _compute_derived(self) -> None:
        self.savings_amount = max(self.monthly_income - self.monthly_expenses, 0.0)
        self.savings_rate = (
            self.savings_amount / self.monthly_income * 100.0
            if self.monthly_income > 0
            else 0.0
        )
        self.net_worth = self.investments + self.liquid_assets - self.debt
        self.expense_coverage_months = (
            self.emergency_fund / self.monthly_expenses
            if self.monthly_expenses > 0
            else 0.0
        )
        self.debt_to_income = (
            self.debt / (self.monthly_income * 12.0)
            if self.monthly_income > 0
            else 0.0
        )

    @classmethod
    def from_raw(
        cls,
        monthly_income: float,
        monthly_expenses: float,
        investments: float,
        liquid_assets: float,
        debt: float,
        emergency_fund: float,
        has_high_interest_debt: bool,
        income_history: list | None = None,
        expense_history: list | None = None,
    ) -> "FinancialSnapshot":
        return cls(
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            investments=investments,
            liquid_assets=liquid_assets,
            debt=debt,
            emergency_fund=emergency_fund,
            has_high_interest_debt=has_high_interest_debt,
            income_history=income_history or [],
            expense_history=expense_history or [],
        )
