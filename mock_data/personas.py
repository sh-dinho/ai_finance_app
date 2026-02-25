from .base import PersonaBase

# Most personas use the base logic.
# Only override if needed.

class CommissionSalesPersona(PersonaBase):
    def generate_monthly_entries(self, profile, months):
        # Same as base, but with stronger commission spikes
        entries = super().generate_monthly_entries(profile, months)
        for e in entries:
            if e.income > profile["income_base"] * 1.5:
                e.income *= 1.2
        return entries


PERSONA_CLASSES = {
    "commission_sales": CommissionSalesPersona,
}