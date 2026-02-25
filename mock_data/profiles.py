from datetime import date

# Persona configuration profiles
# These define the *bounds* and *behavior* for each persona.
# The generator will randomize within these ranges.

PERSONA_PROFILES = {

    "stable_salaried": {
        "income_base": 5200,
        "income_volatility": 0.08,
        "income_seasonality": 0.25,   # bi-weekly paychecks
        "income_trend": "flat",

        "expense_base": 3400,
        "expense_volatility": 0.10,
        "expense_seasonality": 0.10,

        "savings_behavior": "consistent",
        "logging_behavior": "strong",

        "age_range": (28, 50),

        "life_events": {
            "income": ["bonus"],
            "expenses": ["car_repair", "vacation"],
        },

        "goals": [
            ("Emergency Fund", 15000, 2),
            ("Retirement", 200000, 10),
        ],
    },

    "freelancer": {
        "income_base": 4200,
        "income_volatility": 0.55,
        "income_seasonality": 0.10,
        "income_trend": "flat",

        "expense_base": 3000,
        "expense_volatility": 0.35,
        "expense_seasonality": 0.05,

        "savings_behavior": "inconsistent",
        "logging_behavior": "irregular",

        "age_range": (25, 45),

        "life_events": {
            "income": ["dry_spell", "big_contract"],
            "expenses": ["equipment_purchase"],
        },

        "goals": [
            ("Tax Fund", 8000, 1),
            ("Emergency Fund", 10000, 2),
        ],
    },

    "high_earner_spender": {
        "income_base": 11000,
        "income_volatility": 0.15,
        "income_seasonality": 0.10,
        "income_trend": "increasing",

        "expense_base": 9000,
        "expense_volatility": 0.30,
        "expense_seasonality": 0.20,

        "savings_behavior": "low",
        "logging_behavior": "moderate",

        "age_range": (30, 55),

        "life_events": {
            "income": ["bonus"],
            "expenses": ["luxury_purchase", "vacation"],
        },

        "goals": [
            ("Luxury Car", 60000, 3),
            ("Investment Portfolio", 150000, 5),
        ],
    },

    "financially_stressed": {
        "income_base": 3800,
        "income_volatility": 0.25,
        "income_seasonality": 0.05,
        "income_trend": "decreasing",

        "expense_base": 3600,
        "expense_volatility": 0.40,
        "expense_seasonality": 0.10,

        "savings_behavior": "negative",
        "logging_behavior": "weak",

        "age_range": (25, 60),

        "life_events": {
            "income": ["hours_cut"],
            "expenses": ["medical_bill", "car_repair"],
        },

        "goals": [
            ("Debt Payoff", 12000, 3),
            ("Emergency Fund", 5000, 2),
        ],
    },

    "young_investor": {
        "income_base": 4800,
        "income_volatility": 0.12,
        "income_seasonality": 0.10,
        "income_trend": "increasing",

        "expense_base": 2500,
        "expense_volatility": 0.20,
        "expense_seasonality": 0.10,

        "savings_behavior": "high",
        "logging_behavior": "strong",

        "age_range": (22, 35),

        "life_events": {
            "income": ["bonus"],
            "expenses": ["travel"],
        },

        "goals": [
            ("Investment Portfolio", 50000, 3),
            ("Emergency Fund", 8000, 2),
        ],
    },

    "near_retirement": {
        "income_base": 7000,
        "income_volatility": 0.05,
        "income_seasonality": 0.10,
        "income_trend": "flat",

        "expense_base": 4000,
        "expense_volatility": 0.10,
        "expense_seasonality": 0.05,

        "savings_behavior": "high",
        "logging_behavior": "strong",

        "age_range": (55, 65),

        "life_events": {
            "income": ["bonus"],
            "expenses": ["home_repair"],
        },

        "goals": [
            ("Retirement Fund", 500000, 5),
            ("Mortgage Payoff", 80000, 3),
        ],
    },

    "student": {
        "income_base": 1800,
        "income_volatility": 0.40,
        "income_seasonality": 0.05,
        "income_trend": "flat",

        "expense_base": 1600,
        "expense_volatility": 0.30,
        "expense_seasonality": 0.10,

        "savings_behavior": "low",
        "logging_behavior": "weak",

        "age_range": (18, 26),

        "life_events": {
            "income": ["hours_cut"],
            "expenses": ["tuition_payment"],
        },

        "goals": [
            ("Tuition Fund", 15000, 2),
            ("Emergency Fund", 2000, 1),
        ],
    },

    "family_childcare": {
        "income_base": 6500,
        "income_volatility": 0.10,
        "income_seasonality": 0.10,
        "income_trend": "flat",

        "expense_base": 5200,
        "expense_volatility": 0.25,
        "expense_seasonality": 0.20,

        "savings_behavior": "moderate",
        "logging_behavior": "moderate",

        "age_range": (30, 45),

        "life_events": {
            "income": ["bonus"],
            "expenses": ["childcare_spike", "school_fees"],
        },

        "goals": [
            ("Education Fund", 20000, 5),
            ("Emergency Fund", 10000, 2),
        ],
    },

    "commission_sales": {
        "income_base": 3500,
        "income_volatility": 0.70,
        "income_seasonality": 0.40,  # strong seasonality
        "income_trend": "increasing",

        "expense_base": 2800,
        "expense_volatility": 0.25,
        "expense_seasonality": 0.10,

        "savings_behavior": "inconsistent",
        "logging_behavior": "moderate",

        "age_range": (25, 50),

        "life_events": {
            "income": ["commission_spike", "dry_spell"],
            "expenses": ["travel"],
        },

        "goals": [
            ("Car Purchase", 25000, 2),
            ("Emergency Fund", 8000, 2),
        ],
    },

    "seasonal_worker": {
        "income_base": 3000,
        "income_volatility": 0.80,
        "income_seasonality": 0.70,
        "income_trend": "flat",

        "expense_base": 2200,
        "expense_volatility": 0.20,
        "expense_seasonality": 0.10,

        "savings_behavior": "moderate",
        "logging_behavior": "weak",

        "age_range": (20, 55),

        "life_events": {
            "income": ["off_season", "peak_season"],
            "expenses": ["travel"],
        },

        "goals": [
            ("Off-Season Fund", 6000, 1),
            ("Emergency Fund", 5000, 2),
        ],
    },
}