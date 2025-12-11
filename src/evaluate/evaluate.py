# src/evaluate/evaluate.py

from pathlib import Path

from ..utils import load_json, save_json
from ..config import ENCODED_PROMPTS_PATH, RESULTS_DIR, LLM_BACKEND
from ..backend.backend_gemini import run_gemini


def evaluate_corpus():
    """Run evaluation on each encoded prompt using Gemini (or manual GPT)."""
    print(f"Loading encoded prompts from {ENCODED_PROMPTS_PATH}...")
    corpus = load_json(ENCODED_PROMPTS_PATH)

    if not isinstance(corpus, list):
        raise ValueError("encoded_prompts.json must contain a LIST of samples")

    print(f"Loaded {len(corpus)} encoded variants.")

    results = []
    raw_dir = RESULTS_DIR / "gemini_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for record in corpus:
        pid = record["id"]
        cipher = record["cipher"]
        encoded_text = record["encoded_text"]

        print(f"→ Evaluating: ID={pid}, cipher={cipher}")

        if LLM_BACKEND.lower() == "gemini":
            gem = run_gemini(encoded_text)
            gem_raw = gem["raw"]
            gem_clean = gem["clean"]
        else:
            gem_raw = ""
            gem_clean = "(LLM_BACKEND != 'gemini' — no automatic output.)"

        # Save raw response to a text file for transparency
        raw_file = raw_dir / f"{pid}_{cipher}_gemini.txt"
        try:
            raw_file.write_text(gem_raw, encoding="utf-8")
        except Exception as e:
            print(f"  ⚠️ Could not write raw file for {pid}/{cipher}: {e}")

        results.append(
            {
                "id": pid,
                "cipher": cipher,
                "encoded_text": encoded_text,
                "gemini_raw": gem_raw,
                "gemini_clean": gem_clean,
            }
        )

    out_path = RESULTS_DIR / "gemini_results.json"
    save_json(out_path, results)
    print(f"✔ Saved Gemini results → {out_path}")


def main():
    evaluate_corpus()


if __name__ == "__main__":
    main()
