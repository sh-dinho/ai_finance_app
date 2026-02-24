import json
import re
from pathlib import Path
from typing import Dict, Tuple
from functools import lru_cache
from difflib import SequenceMatcher

MEMORY_PATH = "data/transaction_memory.json"


# =====================================================
# Load Categories
# =====================================================

@lru_cache(maxsize=1)
def load_categories(path: str = "data/categories.json") -> Dict[str, list]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# Transaction Memory
# =====================================================

def load_memory() -> Dict:
    path = Path(MEMORY_PATH)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory: Dict):
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def remember_transaction(description: str, category: str):
    """
    Called when user manually corrects a category.
    """
    memory = load_memory()
    key = description.lower().strip()

    if key not in memory:
        memory[key] = {"category": category, "count": 1}
    else:
        memory[key]["category"] = category
        memory[key]["count"] += 1

    save_memory(memory)


# =====================================================
# Helper: Fuzzy Similarity
# =====================================================

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


# =====================================================
# Smart Category Detection (With Memory Override)
# =====================================================

def detect_category(
    description: str,
    categories: Dict[str, list],
    fuzzy_threshold: float = 0.8
) -> Tuple[str, float]:

    if not description:
        return "Other", 0.0

    desc = description.lower().strip()

    # -----------------------------
    # 1️⃣ Check Memory First
    # -----------------------------
    memory = load_memory()
    if desc in memory:
        learned_category = memory[desc]["category"]
        confidence = min(0.9 + (memory[desc]["count"] * 0.01), 0.99)
        return learned_category, round(confidence, 2)

    # -----------------------------
    # 2️⃣ Rule-Based Scoring
    # -----------------------------
    scores = {}

    for category, keywords in categories.items():
        score = 0

        for kw in keywords:
            kw = kw.lower()

            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, desc):
                score += 2
            elif kw in desc:
                score += 1
            elif similarity(desc, kw) >= fuzzy_threshold:
                score += 1

        if score > 0:
            scores[category] = score

    if not scores:
        return "Other", 0.0

    best_category = max(scores, key=scores.get)
    total_score = sum(scores.values())
    confidence = scores[best_category] / total_score if total_score else 0

    return best_category, round(confidence, 2)