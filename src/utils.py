# src/utils.py

import json
from pathlib import Path
from typing import Any, Dict, List

from .config import BASE_PROMPTS_PATH, ENCODED_PROMPTS_PATH


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def ensure_dirs() -> None:
    BASE_PROMPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENCODED_PROMPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
