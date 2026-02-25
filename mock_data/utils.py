import random
import numpy as np
from typing import List, Tuple, Dict

def random_with_volatility(base: float, volatility: float) -> float:
    """Calculates a value within a volatility range using a uniform distribution."""
    return base * (1 + random.uniform(-volatility, volatility))

def apply_trend(value: float, month_index: int, trend: str) -> float:
    """
    Applies a linear trend to a monthly value.
    'increasing' adds 1% monthly compounding, 'decreasing' subtracts 1%.
    """
    if trend == "increasing":
        return value * (1.01 ** month_index)
    if trend == "decreasing":
        return value * (0.99 ** month_index)
    return value

def apply_seasonality(value: float, month_index: int, strength: float) -> float:
    """Applies a sine-wave based seasonality factor (12-month cycle)."""
    return value * (1 + strength * np.sin(month_index * np.pi / 6))

def pick_life_events(events: Dict[str, List[str]], months: int) -> List[Tuple[str, int]]:
    """Randomly assigns life events to specific months in the timeline."""
    chosen = []
    for category, ev_list in events.items():
        if random.random() < 0.4:
            # Pick one event from category and a random month
            chosen.append((random.choice(ev_list), random.randint(0, months - 1)))
    return chosen