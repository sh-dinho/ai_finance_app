import copy
from typing import Dict, Any
from .profiles import PERSONA_PROFILES
from .personas import PERSONA_CLASSES
from .base import PersonaBase

def generate_mock_persona(name: str, months: int = 24, **overrides) -> Dict[str, Any]:
    """
    Primary API for mock data generation.
    Refactored to ensure that overrides do not mutate the base PERSONA_PROFILES.
    """
    if name not in PERSONA_PROFILES:
        raise ValueError(f"Persona '{name}' not found. Available: {list(PERSONA_PROFILES.keys())}")

    # Use deepcopy to prevent cross-run data contamination
    profile = copy.deepcopy(PERSONA_PROFILES[name])

    # Apply user-defined overrides
    for key, value in overrides.items():
        profile[key] = value

    # Strategy pattern: select the specific persona class or default to base
    persona_cls = PERSONA_CLASSES.get(name, PersonaBase)
    instance = persona_cls()

    return instance.generate(profile, months=months)