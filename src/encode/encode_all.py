# src/encode/encode_all.py

import random
from typing import Dict
from ..utils import load_json, save_json, ensure_dirs
from ..config import BASE_PROMPTS_PATH, ENCODED_PROMPTS_PATH

# -----------------------------------------------------------
# BASIC CIPHERS
# -----------------------------------------------------------

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def caesar(text: str, shift: int = 3) -> str:
    out = []
    for c in text:
        if c.isalpha():
            base = "A" if c.isupper() else "a"
            offset = (ord(c) - ord(base) + shift) % 26
            out.append(chr(ord(base) + offset))
        else:
            out.append(c)
    return "".join(out)


def vigenere(text: str, key: str = "KEY") -> str:
    out = []
    key = key.lower()
    klen = len(key)
    j = 0
    for c in text:
        if c.isalpha():
            base = "A" if c.isupper() else "a"
            k = ord(key[j % klen]) - ord("a")
            offset = (ord(c) - ord(base) + k) % 26
            out.append(chr(ord(base) + offset))
            j += 1
        else:
            out.append(c)
    return "".join(out)


def generate_substitution_mapping(seed: int = 42) -> Dict[str, str]:
    random.seed(seed)
    letters = list(ALPHABET)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))


SUB_MAP = generate_substitution_mapping()


def substitution(text: str, mapping: Dict[str, str] = SUB_MAP) -> str:
    out = []
    for c in text:
        lower = c.lower()
        if lower in mapping:
            sub = mapping[lower]
            out.append(sub.upper() if c.isupper() else sub)
        else:
            out.append(c)
    return "".join(out)


# -----------------------------------------------------------
# EMOJI CIPHER
# -----------------------------------------------------------

EMOJI_MAP = {
    "a": "😀",
    "b": "😃",
    "c": "😄",
    "d": "😁",
    "e": "😆",
    "f": "😅",
    "g": "🤣",
    "h": "😊",
    "i": "😇",
    "j": "🙂",
    "k": "🙃",
    "l": "😉",
    "m": "😌",
    "n": "😍",
    "o": "😘",
    "p": "😜",
    "q": "🤓",
    "r": "😎",
    "s": "😤",
    "t": "😱",
    "u": "🤯",
    "v": "😈",
    "w": "👻",
    "x": "🤖",
    "y": "👽",
    "z": "🧠",
}


def emoji_encode(text: str) -> str:
    return "".join(EMOJI_MAP.get(c.lower(), c) for c in text)


# -----------------------------------------------------------
# ZERO-WIDTH STEGANOGRAPHY
# -----------------------------------------------------------

ZERO_WIDTH_SPACE = "\u200b"
ZERO_WIDTH_JOINER = "\u200d"


def zero_width_stego(text: str) -> str:
    """Insert zero-width characters between letters."""
    out = []
    for i, c in enumerate(text):
        out.append(c)
        if c != " ":
            z = ZERO_WIDTH_SPACE if i % 2 == 0 else ZERO_WIDTH_JOINER
            out.append(z)
    return "".join(out)


# -----------------------------------------------------------
# ADVANCED CIPHERS (FOR HIGHER SEVERITY SCORES)
# -----------------------------------------------------------

# Homoglyph substitution (Cyrillic look-alikes)
HOMOGLYPH_MAP = {
    "a": "а",
    "e": "е",
    "o": "о",
    "p": "р",
    "c": "с",
    "x": "х",
    "y": "у",
    "h": "һ",
}


def homoglyph_encode(text: str) -> str:
    out = []
    for c in text:
        cl = c.lower()
        if cl in HOMOGLYPH_MAP:
            out.append(HOMOGLYPH_MAP[cl])
        else:
            out.append(c)
    return "".join(out)


def caesar_chain(text: str) -> str:
    """Chain 3 Caesar ciphers to make decoding harder."""
    return caesar(caesar(caesar(text, 3), 11), 7)


def vigenere_nl(text: str) -> str:
    """Vigenère using a natural-language key."""
    return vigenere(text, key="security")


def hybrid_stego(text: str) -> str:
    """Combine homoglyph + zero-width characters."""
    return zero_width_stego(homoglyph_encode(text))


# -----------------------------------------------------------
# MASTER ENCODING FUNCTION
# -----------------------------------------------------------


def generate_all_encodings(text: str) -> Dict[str, str]:
    """Return dictionary of all encoded variants for one prompt."""
    return {
        "plain": text,
        "caesar": caesar(text),
        "vigenere": vigenere(text),
        "substitution": substitution(text),
        "emoji": emoji_encode(text),
        "stego": zero_width_stego(text),
        "caesar_chain": caesar_chain(text),
        "vigenere_nl": vigenere_nl(text),
        "homoglyph": homoglyph_encode(text),
        "hybrid_stego": hybrid_stego(text),
    }


# -----------------------------------------------------------
# BUILD FULL ENCODED CORPUS
# -----------------------------------------------------------


def main():
    ensure_dirs()

    base = load_json(BASE_PROMPTS_PATH)
    encoded_list = []

    for item in base:
        pid = item["id"]
        text = item["text"]

        encodings = generate_all_encodings(text)

        for cipher_name, encoded_text in encodings.items():
            encoded_list.append(
                {
                    "id": pid,
                    "cipher": cipher_name,
                    "encoded_text": encoded_text,
                }
            )

    save_json(ENCODED_PROMPTS_PATH, encoded_list)
    print(f"✔ Encoded corpus saved → {ENCODED_PROMPTS_PATH}")


if __name__ == "__main__":
    main()
