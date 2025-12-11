# src/diagnose_prompts.py
import json
from src.config import ENCODED_PROMPTS_PATH

with open(ENCODED_PROMPTS_PATH, "r", encoding="utf-8") as f:
    prompts = json.load(f)

print("Total prompts:", len(prompts))
