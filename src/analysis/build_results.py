# src/analysis/build_results.py

import json
import csv
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_gemini_result(item):
    """Convert Gemini result format into a standard structure."""
    return {
        "prompt_id": item["prompt_id"],
        "cipher": item["cipher"],
        "model": "Gemini",
        "input_text": item["input_text"],
        "response_text": item["response"] if item.get("success") else "",
        "error": item["error"] if not item.get("success") else "",
    }


def normalize_chatgpt_result(item):
    """Convert ChatGPT parsed Word doc entry into standard structure."""
    return {
        "prompt_id": item["prompt_id"],
        "cipher": item["cipher"],
        "model": "ChatGPT",
        "input_text": item["encoded_prompt"],
        "response_text": item.get("chatgpt_response", ""),
        "error": "",
    }


def build_combined_results():
    print("🔍 Loading raw model outputs...")

    gemini_results = load_json("results/gemini_results.json")
    chatgpt_results = load_json("results/chatgpt_results.json")

    combined = []

    # Normalize Gemini results
    for item in gemini_results:
        combined.append(normalize_gemini_result(item))

    # Normalize ChatGPT results
    for item in chatgpt_results:
        combined.append(normalize_chatgpt_result(item))

    Path("results").mkdir(exist_ok=True)

    # Save JSON
    json_path = "results/combined_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=4, ensure_ascii=False)

    # Save CSV
    csv_path = "results/combined_results.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=combined[0].keys())
        writer.writeheader()
        writer.writerows(combined)

    print(f"✔ Combined results saved → {json_path}")
    print(f"✔ Combined results saved → {csv_path}")

    return combined


def main():
    build_combined_results()


if __name__ == "__main__":
    main()
