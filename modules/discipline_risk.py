import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


# =====================================================
# Public API
# =====================================================

def calculate_discipline_risk(
    df: pd.DataFrame,
    budget_comparison: Optional[Dict[str, Any]] = None,
    *,
    savings_decline_window: int = 6,
    volatility_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Evaluate financial discipline risk based on spending, savings,
    volatility, and budget adherence.

    Returns:
        {
            "risk_score": int (0–100),
            "risk_level": str,
            "risk_factors": list[str]
        }
    """

    logger.debug("Starting discipline risk evaluation")

    if df.empty:
        logger.warning("Empty dataframe passed to discipline risk engine")
        return _empty_result()

    df = df.copy()

    # Clean numeric columns
    for col in ["income", "expenses", "savings"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    risk_score = 0
    risk_factors: List[str] = []

    # -------------------------------------------------
    # 1️⃣ Negative Savings Frequency
    # -------------------------------------------------
    if "savings" in df.columns:
        negative_ratio = (df["savings"] < 0).mean()
        logger.debug(f"Negative savings ratio: {negative_ratio:.2f}")

        if negative_ratio > 0.4:
            risk_score += 25
            risk_factors.append("Frequent negative savings months")
        elif negative_ratio > 0.2:
            risk_score += 15
            risk_factors.append("Occasional negative savings months")

    # -------------------------------------------------
    # 2️⃣ Savings Rate Decline (trend-based)
    # -------------------------------------------------
    if "income" in df.columns and "expenses" in df.columns:
        df["savings_rate"] = (
            (df["income"] - df["expenses"]) / df["income"]
        ).replace([np.inf, -np.inf], 0).fillna(0)

        if len(df) >= savings_decline_window:
            half = savings_decline_window // 2
            recent = df["savings_rate"].tail(half).mean()
            previous = df["savings_rate"].iloc[-savings_decline_window:-half].mean()

            logger.debug(f"Savings rate trend — previous: {previous:.2f}, recent: {recent:.2f}")

            if recent < previous:
                decline = previous - recent
                penalty = min(20, decline * 100)
                risk_score += penalty
                risk_factors.append(f"Savings rate declining ({decline:.2f} drop)")

    # -------------------------------------------------
    # 3️⃣ Expense Volatility
    # -------------------------------------------------
    if "expenses" in df.columns:
        mean_exp = df["expenses"].mean()
        if mean_exp > 0:
            volatility = df["expenses"].std()
            volatility_ratio = volatility / mean_exp

            logger.debug(f"Expense volatility ratio: {volatility_ratio:.2f}")

            if volatility_ratio > volatility_threshold:
                risk_score += 15
                risk_factors.append(
                    f"High expense volatility (ratio {volatility_ratio:.2f})"
                )

    # -------------------------------------------------
    # 4️⃣ Budget Breaches
    # -------------------------------------------------
    if budget_comparison:
        over_budget_count = sum(
            1 for v in budget_comparison.values()
            if v.get("status") == "Over Budget"
        )

        logger.debug(f"Over-budget categories: {over_budget_count}")

        if over_budget_count >= 3:
            risk_score += 20
            risk_factors.append("Multiple categories over budget")
        elif over_budget_count > 0:
            risk_score += 10
            risk_factors.append("Some categories over budget")

    # -------------------------------------------------
    # Normalize Score
    # -------------------------------------------------
    risk_score = min(100, int(risk_score))
    risk_level = _classify_risk(risk_score)

    logger.info(f"Discipline risk evaluation complete — Score: {risk_score}, Level: {risk_level}")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }


# =====================================================
# Helpers
# =====================================================

def _classify_risk(score: int) -> str:
    """Map numeric score to qualitative risk level."""
    if score < 25:
        return "Low"
    elif score < 50:
        return "Moderate"
    elif score < 75:
        return "High"
    return "Critical"


def _empty_result() -> Dict[str, Any]:
    """Return default result for empty datasets."""
    return {
        "risk_score": 0,
        "risk_level": "Low",
        "risk_factors": []
    }