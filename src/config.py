# src/config.py

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# ----------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

BASE_PROMPTS_PATH = DATA_DIR / "corpus.json"
ENCODED_PROMPTS_PATH = DATA_DIR / "encoded_prompts.json"

ZERO_SHOT_RESULTS_PATH = RESULTS_DIR / "zero_shot_results.csv"
FEW_SHOT_RESULTS_PATH = RESULTS_DIR / "few_shot_results.csv"
DEFENSE_RESULTS_PATH = RESULTS_DIR / "defense_results.csv"

# ----------------------------------------------------
# LLM SELECTION
# ----------------------------------------------------

LLM_BACKEND = os.getenv("LLM_BACKEND", "gemini")

# ----------------------------------------------------
# GEMINI CONFIG
# ----------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-live-preview")
