from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class FISReport:
    intelligence: Dict[str, Any]
    insights: Dict[str, Any]
