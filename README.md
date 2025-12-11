# Cypher-Based Social Engineering Prompts

This project investigates whether large language models (LLMs) follow **obfuscated, potentially harmful social-engineering instructions** when those instructions are hidden with simple ciphers or steganography.

All prompts are written in **high-level, non-actionable form**, suitable for **defensive security research and academic analysis**.

## Components

- `data/base_prompts.json` – neutral, research-style prompts (English + Latin).
- `data/encoded_prompts.json` – automatically generated ciphered variants.
- `src/encode_all.py` – builds ciphered corpus (Caesar, Vigenère, substitution, emoji, zero-width).
- `src/evaluate.py` – runs zero-shot and few-shot evaluations against chosen LLMs.
- `src/detect_cipher.py` – lightweight heuristic cipher/stego detector.
- `src/canonicalize.py` – canonicalization & sanitization of user text.
- `src/defense_wrapper.py` – simple defensive wrapper using detector + canonicalizer.

## Quickstart

1. Generate the base corpus:
   ```bash
   python src/build_corpus.py
   ```
