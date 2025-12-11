# src/defense_wrapper.py

from .detect_cipher import classify_cipher
from .canonicalize import canonicalize


def defensive_wrapper(user_input: str) -> str:
    """
    If input looks encoded/obfuscated, ask for a plain-language restatement.
    Otherwise, return canonicalized text.
    """
    cipher_class = classify_cipher(user_input)

    if cipher_class != "plain":
        return (
            "Your message appears to be encoded, obfuscated, or steganographic. "
            "For safety, please restate your request in clear, plain language without "
            "any ciphers or hidden content."
        )

    return canonicalize(user_input)
