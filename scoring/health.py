from scoring.utils import clamp, pct


def financial_health_score(snapshot, settings):
    w = settings.weights.health.weights

    cashflow_score = clamp(pct(snapshot.savings_amount, snapshot.monthly_income))
    emergency_score = clamp(pct(snapshot.emergency_fund, snapshot.monthly_expenses * 3))
    debt_score = 100.0 if not snapshot.has_high_interest_debt else clamp(100 - pct(snapshot.debt, snapshot.monthly_income * 12))
    investing_score = clamp(pct(snapshot.investments, snapshot.monthly_income * 12))

    final_score = (
        cashflow_score * w.cashflow +
        emergency_score * w.emergency +
        debt_score * w.debt +
        investing_score * w.investing
    )

    return {
        "cashflow_score": cashflow_score,
        "emergency_score": emergency_score,
        "debt_score": debt_score,
        "investing_score": investing_score,
        "final_score": clamp(final_score),
    }
