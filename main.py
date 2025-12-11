# main.py

import argparse
import subprocess
import time
from pathlib import Path

# ---------- Helper ----------
def run(cmd):
    print(f"\n=== RUNNING: {cmd} ===")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error: {e}")
    print()


def wait_for_file(path):
    print("\n--- ChatGPT Manual Step Required ---")
    print(f"Paste ChatGPT outputs into:\n  {path}")
    print("This will continue when the file exists.\n")

    while not Path(path).exists():
        print(f"⏳ Waiting for: {path}")
        time.sleep(3)

    print("✔ File detected — continuing.\n")


# ---------- Pipeline Commands ----------

def step_build():
    run("python -m src.corpus.build_corpus")

def step_encode():
    run("python -m src.encode.encode_all")

def step_gemini():
    run("python -m src.evaluate.evaluate")

def step_chatgpt():
    responses_path = "report/llm_responses.docx"
    wait_for_file(responses_path)
    run("python -m src.evaluate.read_results")

def step_combine():
    run("python -m src.analysis.build_results")

def step_score():
    run("python -m src.analysis.severity_scoring")

def step_graphs():
    run("python -m src.analysis.visualization")

def step_confusion():
    run("python -m src.analysis.confusion_matrix")

def step_pdf():
    run("python -m src.analysis.generate_pdf_report")


# ---------- Run Full Pipeline ----------
def step_all():
    step_build()
    step_encode()
    step_gemini()
    step_chatgpt()
    step_combine()
    step_score()
    step_graphs()
    step_confusion()
    step_pdf()


# ---------- CLI Setup ----------
def main():
    parser = argparse.ArgumentParser(
        description="CYBER 221 - Cipher LLM Testing Toolkit"
    )

    parser.add_argument(
        "command",
        choices=[
            "build", "encode", "gemini", "chatgpt",
            "combine", "score", "graphs", "confusion",
            "pdf", "all"
        ],
        help="Pipeline step to run"
    )

    args = parser.parse_args()

    command_map = {
        "build": step_build,
        "encode": step_encode,
        "gemini": step_gemini,
        "chatgpt": step_chatgpt,
        "combine": step_combine,
        "score": step_score,
        "graphs": step_graphs,
        "confusion": step_confusion,
        "pdf": step_pdf,
        "all": step_all,
    }

    command_map[args.command]()


if __name__ == "__main__":
    main()
