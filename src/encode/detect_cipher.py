# src/detect_cipher.py

from collections import Counter
from math import log2
from typing import Literal

ZERO_WIDTH_CHARS = {
    "\u200b",  # zero-width space
    "\u200c",  # zero-width non-joiner
    "\u200d",  # zero-width joiner
    "\ufeff",  # zero-width no-break space
}


def contains_zero_width(text: str) -> bool:
    return any(c in ZERO_WIDTH_CHARS for c in text)


def contains_many_emojis(text: str, threshold: int = 5) -> bool:
    count = 0
    for c in text:
        if 0x1F300 <= ord(c) <= 0x1FAFF:
            count += 1
            if count >= threshold:
                return True
    return False


def shannon_entropy(text: str) -> float:
    filtered = [c.lower() for c in text if c.isalpha()]
    if not filtered:
        return 0.0
    counts = Counter(filtered)
    total = len(filtered)
    probs = [c / total for c in counts.values()]
    return -sum(p * log2(p) for p in probs)


def classify_cipher(
    text: str,
) -> Literal["plain", "emoji", "zero_width", "high_entropy", "unknown"]:
    if contains_zero_width(text):
        return "zero_width"
    if contains_many_emojis(text):
        return "emoji"

    ent = shannon_entropy(text)
    # Very rough heuristic:
    # natural language ~3.5–4.5 bits; higher entropy can indicate substitution / Vigenère
    if ent > 4.5:
        return "high_entropy"

    return "plain"
