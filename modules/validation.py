from .models import FinancialDataBundle

def validate_bundle(bundle: FinancialDataBundle):
    """Checks if the data bundle has the minimum required information."""
    if bundle.df_daily.empty:
        raise ValueError("Daily transaction data is missing.")
    if not bundle.entries:
        raise ValueError("Monthly log entries are missing.")
    if bundle.snapshot.monthly_income <= 0:
        raise ValueError("Monthly income must be greater than zero for ratio analysis.")