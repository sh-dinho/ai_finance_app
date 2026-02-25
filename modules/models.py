# modules/models.py

from dataclasses import dataclass
from typing import Dict, Any, List
import pandas as pd

from .core import FinancialSnapshot, MonthlyLogEntry


@dataclass
class FinancialDataBundle:
    snapshot: FinancialSnapshot
    entries: List[MonthlyLogEntry]
    df_daily: pd.DataFrame
    goals: Dict[str, Dict[str, Any]]
    current_goal_values: Dict[str, float]
    monthly_savings: float = 0.0
    budget_comparison: Dict[str, Any] | None = None
    age: int = 30


@dataclass
class FISReport:
    ratios: Dict[str, Any]
    emergency_fund: Dict[str, Any]
    income_insights: Dict[str, Any]
    trend_insights: Dict[str, Any]
    forecast: Dict[str, Any]
    discipline_risk: Dict[str, Any]
    habits: Dict[str, Any]
    goals: Dict[str, Any]
    goal_insights: Dict[str, Any]
    intelligence_score: Dict[str, Any]


@dataclass
class FISPipelineOutput:
    """
    Structured output returned by the FIS pipeline when return_dict=False.
    """
    fis_report: FISReport
    recommendations: Dict[str, Any]