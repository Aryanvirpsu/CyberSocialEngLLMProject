# src/evaluate/read_results.py

import json
from pathlib import Path
from docx import Document


def parse_llm_doc(path="report/llm_responses.docx"):
    doc = Document(path)

    results = []
    current = {}

    for para in doc.paragraphs:
        text = para.text.strip()

        if text.startswith("Prompt ID:"):
            if current:
                results.append(current)
            current = {"prompt_id": text.split(":")[1].strip()}

        elif text.startswith("Cipher:"):
            current["cipher"] = text.split(":")[1].strip()

        elif text.startswith("Encoded Prompt:"):
            current["encoded_prompt"] = ""

        elif current.get("encoded_prompt") == "":
            # next lines until separator
            current["encoded_prompt"] = text

        elif text.startswith("ChatGPT Response:"):
            current["chatgpt_response"] = ""

        elif "chatgpt_response" in current and current["chatgpt_response"] == "":
            current["chatgpt_response"] = text

        elif text == "---":
            results.append(current)
            current = {}

    # push last entry
    if current:
        results.append(current)

    return results


def save_results(data, out="results/chatgpt_results.json"):
    Path("results").mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✔ Saved ChatGPT results → {out}")


def main():
    parsed = parse_llm_doc()
    save_results(parsed)


if __name__ == "__main__":
    main()
