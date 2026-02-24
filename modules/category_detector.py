import json
import re
from pathlib import Path
from typing import Dict, Tuple
from functools import lru_cache
from difflib import SequenceMatcher


# =====================================================
# Load Categories (Cached)
# =====================================================

@lru_cache(maxsize=1)
def load_categories(path: str = "data/categories.json") -> Dict[str, list]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Categories file not found: {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# Helper: Fuzzy Matching
# =====================================================

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


# =====================================================
# Smart Category Detection
# =====================================================

def detect_category(
    description: str,
    categories: Dict[str, list],
    fuzzy_threshold: float = 0.8
) -> Tuple[str, float]:
    """
    Returns:
        (category_name, confidence_score)
    """

    if not description:
        return "Other", 0.0

    desc = description.lower().strip()

    scores = {}

    # -----------------------------
    # Exact & Word Boundary Matching
    # -----------------------------
    for category, keywords in categories.items():
        score = 0

        for kw in keywords:
            kw = kw.lower()

            # Exact word boundary match
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, desc):
                score += 2

            # Partial match
            elif kw in desc:
                score += 1

            # Fuzzy match
            else:
                if similarity(desc, kw) >= fuzzy_threshold:
                    score += 1

        if score > 0:
            scores[category] = score

    if not scores:
        return "Other", 0.0

    # -----------------------------
    # Select Highest Score
    # -----------------------------
    best_category = max(scores, key=scores.get)
    total_score = sum(scores.values())
    confidence = scores[best_category] / total_score if total_score else 0

    return best_category, round(confidence, 2)