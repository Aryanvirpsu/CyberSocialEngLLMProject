# src/canonicalize.py

from typing import Optional, Dict
import unicodedata

from .detect_cipher import ZERO_WIDTH_CHARS


def remove_zero_width(text: str) -> str:
    return "".join(c for c in text if c not in ZERO_WIDTH_CHARS)


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def replace_emojis_with_token(text: str, token: str = "<EMOJI>") -> str:
    result = []
    for c in text:
        if 0x1F300 <= ord(c) <= 0x1FAFF:
            result.append(token)
        else:
            result.append(c)
    return "".join(result)

def canonicalize(text: Optional[str], options: Optional[Dict] = None) -> str:
    """
    Basic canonicalization:
    - Unicode normalization
    - Remove zero-width characters
    - Replace emojis with tokens
    - Lowercase
    Always returns a STRING, even if input is None.
    """

    # Handle None safely (fixes your error)
    if text is None:
        return ""

    if options is None:
        options = {}

    t = normalize_unicode(text)
    t = remove_zero_width(t)
    t = replace_emojis_with_token(t)
    t = t.lower()

    return t
