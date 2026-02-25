import json
import re
from pathlib import Path
from typing import Dict, Tuple, Any
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

def load_memory() -> Dict[str, Any]:
    path = Path(MEMORY_PATH)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory: Dict[str, Any]):
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def remember_transaction(description: str, category: str):
    """
    Called when user manually corrects a category.
    Stores normalized description for future matching.
    """
    memory = load_memory()
    key = normalize_text(description)

    if key not in memory:
        memory[key] = {"category": category, "count": 1}
    else:
        memory[key]["category"] = category
        memory[key]["count"] += 1

    save_memory(memory)


# =====================================================
# Helpers
# =====================================================

def normalize_text(text: str) -> str:
    """Lowercase, strip, remove extra spaces."""
    return re.sub(r"\s+", " ", text.lower().strip())


def similarity(a: str, b: str) -> float:
    """Fuzzy similarity score."""
    return SequenceMatcher(None, a, b).ratio()


def tokenize(text: str) -> list:
    """Split into words for more flexible matching."""
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


# =====================================================
# Smart Category Detection
# =====================================================

def detect_category(
    description: str,
    categories: Dict[str, list],
    fuzzy_threshold: float = 0.8,
    debug: bool = False
) -> Tuple[str, float]:

    if not description or not description.strip():
        return "Other", 0.0

    desc = normalize_text(description)
    tokens = tokenize(desc)

    # -----------------------------
    # 1️⃣ Memory Override
    # -----------------------------
    memory = load_memory()
    if desc in memory:
        learned_category = memory[desc]["category"]
        confidence = min(0.9 + (memory[desc]["count"] * 0.02), 0.99)
        return learned_category, round(confidence, 2)

    # -----------------------------
    # 2️⃣ Rule-Based + Fuzzy Scoring
    # -----------------------------
    scores: Dict[str, float] = {}

    for category, keywords in categories.items():
        score = 0.0

        for kw in keywords:
            kw_norm = normalize_text(kw)

            # Exact word match
            if kw_norm in tokens:
                score += 3.0

            # Substring match
            elif kw_norm in desc:
                score += 1.5

            # Fuzzy match
            else:
                sim = similarity(desc, kw_norm)
                if sim >= fuzzy_threshold:
                    score += sim  # weighted by similarity

        # Penalize misleading matches (e.g., "gas" inside "vegas")
        if any(kw in desc for kw in ["vegas", "gasoline"]):
            if category == "Transportation":
                score += 0.5
            else:
                score -= 0.5

        if score > 0:
            scores[category] = score

    if not scores:
        return "Other", 0.0

    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_category, best_score = sorted_scores[0]

    total_score = sum(scores.values())
    confidence = best_score / total_score if total_score else 0.0

    # Scale confidence to feel more natural
    confidence = min(1.0, max(0.05, confidence * 1.2))

    if debug:
        print("DEBUG — Category Scores:", scores)
        print("DEBUG — Best:", best_category, confidence)

    return best_category, round(confidence, 2)