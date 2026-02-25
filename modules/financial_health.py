from typing import Optional, Dict


# =====================================================
# Sub-scores
# =====================================================

def cashflow_score(savings_rate: float) -> int:
    """
    Score based on monthly savings rate.

    0–10%   → low cashflow strength
    10–25%  → moderate
    25%+    → strong
    """
    if savings_rate <= 0:
        return 0
    if savings_rate < 0.10:
        return 40
    if savings_rate < 0.25:
        return 70
    return 100


def emergency_score(emergency_months: float) -> int:
    """
    Score based on emergency fund coverage.

    0 months     → 0
    <1 month     → 30
    1–3 months   → 60
    3+ months    → 100
    """
    if emergency_months <= 0:
        return 0
    if emergency_months < 1:
        return 30
    if emergency_months < 3:
        return 60
    return 100


def debt_health_score(has_high_interest_debt: bool, liquid_to_debt: Optional[float]) -> int:
    """
    Score based on high-interest debt and liquidity ratio.

    liquid_to_debt = liquid_assets / total_debt

    High-interest debt → automatic penalty
    Otherwise, liquidity ratio determines score
    """
    if has_high_interest_debt:
        return 20

    if liquid_to_debt is None:
        return 100

    if liquid_to_debt < 0.5:
        return 40
    if liquid_to_debt < 1:
        return 70
    return 100


def investing_readiness_score(is_investing: bool, emergency_months: float) -> int:
    """
    Score based on investing habits and emergency fund strength.

    Investing without emergency fund → penalized
    Investing with 3+ months saved → strong
    """
    if not is_investing:
        return 40
    if emergency_months < 3:
        return 60
    return 100


# =====================================================
# Composite Financial Health Score
# =====================================================

def financial_health_score(
    cashflow: int,
    savings: int,
    emergency: int,
    debt: int,
    investing: int
) -> Dict[str, int | str]:
    """
    Calculates weighted financial health score (0–100) and status.

    Weights:
        - Cashflow: 25%
        - Savings: 25%
        - Emergency Fund: 20%
        - Debt Health: 20%
        - Investing Readiness: 10%
    """
    score = (
        cashflow * 0.25 +
        savings * 0.25 +
        emergency * 0.20 +
        debt * 0.20 +
        investing * 0.10
    )

    score = round(score)

    if score < 40:
        status = "Poor"
    elif score < 60:
        status = "Fair"
    elif score < 80:
        status = "Good"
    else:
        status = "Excellent"

    return {
        "score": score,
        "status": status
    }