# src/analysis/visualization.py

import json
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path


def load_data(path="results/final_scored_results.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def severity_distribution(rows):
    sev = [r["severity"] for r in rows]
    c = Counter(sev)

    plt.figure(figsize=(6,4))
    plt.bar(c.keys(), c.values())
    plt.title("Severity Distribution")
    plt.xlabel("Severity Level")
    plt.ylabel("Count")
    plt.savefig("results/severity_distribution.png")
    plt.close()


def model_comparison(rows):
    sev = {}
    for r in rows:
        sev.setdefault(r["model"], []).append(r["severity"])

    avg = {m: sum(v)/len(v) for m, v in sev.items()}

    plt.figure(figsize=(6,4))
    plt.bar(avg.keys(), avg.values())
    plt.title("Average Severity by Model")
    plt.ylabel("Average Severity")
    plt.savefig("results/model_comparison.png")
    plt.close()


def cipher_ranking(rows):
    cipher_scores = {}
    for r in rows:
        cipher_scores.setdefault(r["cipher"], []).append(r["severity"])

    avg = {c: sum(v)/len(v) for c, v in cipher_scores.items()}

    plt.figure(figsize=(7,4))
    plt.bar(avg.keys(), avg.values())
    plt.title("Average Severity by Cipher Type")
    plt.ylabel("Severity")
    plt.savefig("results/cipher_ranking.png")
    plt.close()


def main():
    Path("results").mkdir(exist_ok=True)
    rows = load_data()
    severity_distribution(rows)
    model_comparison(rows)
    cipher_ranking(rows)
    print("✔ Graphs saved to /results")


if __name__ == "__main__":
    main()
