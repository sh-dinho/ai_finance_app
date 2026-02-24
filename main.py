from modules.core import calculate_basic_metrics
from modules.core import FinancialEngine

metrics = calculate_basic_metrics(user)

ratios = FinancialEngine.calculate_ratios(metrics)
emergency = FinancialEngine.emergency_fund_coverage(user, metrics)
fire_number = FinancialEngine.calculate_fire_number(metrics["annual_expenses"])
projection = FinancialEngine.project_net_worth(metrics["net_worth"], metrics["savings"])
stress = FinancialEngine.calculate_stress_index(metrics, emergency["status"])