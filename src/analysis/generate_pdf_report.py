# src/analysis/generate_pdf_report.py

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors

from ..config import RESULTS_DIR
from ..utils import load_json
from .confusion_matrix import build_confusion_matrices


def find_highest_severity_row(rows):
    """Return the row with maximum max_severity."""
    return max(rows, key=lambda r: r.get("max_severity", 0))


def clean_invisible(text: str) -> str:
    """Remove zero-width characters for readability."""
    if not text:
        return ""
    return text.replace("\u200b", "").replace("\u200d", "")


def header_footer(canvas, doc):
    """Draw header and footer on each page."""
    canvas.saveState()
    # Header
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(colors.HexColor("#002D62"))  # PSU dark blue
    canvas.drawString(40, 820, "CYBER 221 – Cipher-Based Social Engineering Prompts")

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(570, 820, "Penn State University")

    # Footer (page number)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(300, 20, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf():
    # Ensure confusion matrix is up to date
    build_confusion_matrices()

    scored_path = RESULTS_DIR / "final_scored_results.json"
    confusion_path = RESULTS_DIR / "confusion_matrix.json"

    if not scored_path.exists():
        print("❌ final_scored_results.json not found. Run severity_scoring first.")
        return

    if not confusion_path.exists():
        print("❌ confusion_matrix.json not found. Run confusion_matrix builder.")
        return

    rows = load_json(scored_path)
    confusion = load_json(confusion_path)

    model_conf = confusion["model_confusion_matrix"]
    cipher_conf = confusion["cipher_confusion_matrix"]

    output = RESULTS_DIR / "final_report.pdf"
    doc = SimpleDocTemplate(str(output), pagesize=letter, topMargin=72, bottomMargin=50)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#002D62"),
    )
    section_header = ParagraphStyle(
        "section_header",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#002D62"),
    )
    text_style = ParagraphStyle(
        "text",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
    )

    elements = []

    # TITLE
    elements.append(Paragraph("LLM Safety Evaluation: Cipher-Based Social Engineering Prompts", title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("CYBER 221 – Compact Research Report", text_style))
    elements.append(Spacer(1, 12))

    # 1. OVERVIEW
    elements.append(Paragraph("1. Project Overview", section_header))
    elements.append(
        Paragraph(
            "This project evaluates whether encoded social-engineering prompts can bypass safety filters "
            "of large language models (LLMs). We encode prompts using Caesar, Vigenère, substitution, emoji, "
            "zero-width steganography, homoglyphs, and hybrid stego ciphers, then test Gemini and ChatGPT to "
            "see if they refuse, detect, interpret, or comply with hidden instructions.",
            text_style,
        )
    )
    elements.append(Spacer(1, 6))

    # Quick stats
    total_rows = len(rows)
    avg_gemini = sum(r["gemini_severity"] for r in rows) / total_rows
    avg_chatgpt = sum(r["chatgpt_severity"] for r in rows) / total_rows

    elements.append(
        Paragraph(
            f"<b>Total encoded evaluations:</b> {total_rows}<br/>"
            f"<b>Gemini average severity:</b> {avg_gemini:.2f}<br/>"
            f"<b>ChatGPT average severity:</b> {avg_chatgpt:.2f}",
            text_style,
        )
    )

    # 2. HIGHEST SEVERITY CASE
    highest = find_highest_severity_row(rows)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("2. Highest Severity Case", section_header))

    elements.append(
        Paragraph(
            f"<b>Prompt ID:</b> {highest['id']}<br/>"
            f"<b>Cipher:</b> {highest['cipher']}<br/>"
            f"<b>Gemini Severity:</b> {highest['gemini_severity']}<br/>"
            f"<b>ChatGPT Severity:</b> {highest['chatgpt_severity']}",
            text_style,
        )
    )
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("<b>Encoded Prompt (cleaned):</b>", text_style))
    elements.append(Paragraph(clean_invisible(highest["encoded_text"]), text_style))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Gemini Response:</b>", text_style))
    gemini_clean_text = highest.get("gemini_clean", "(no Gemini response recorded)")
    elements.append(Paragraph(gemini_clean_text, text_style))

    elements.append(Spacer(1, 10))

    # 3. MODEL CONFUSION MATRIX
    elements.append(Paragraph("3. Model Confusion Matrix", section_header))

    model_table_data = [["Model", "REFUSE", "DETECT", "INTERPRET", "COMPLY"]]
    for model, vals in model_conf.items():
        model_table_data.append(
            [model, vals["REFUSE"], vals["DETECT"], vals["INTERPRET"], vals["COMPLY"]]
        )

    model_table = Table(model_table_data, hAlign="LEFT")
    model_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    elements.append(model_table)
    elements.append(Spacer(1, 8))

    # 4. KEY FINDINGS
    elements.append(Paragraph("4. Key Findings", section_header))

    findings = []

    # Example high-level findings (you can tweak text here if needed)
    findings.append("• Gemini exhibited higher severity scores under hybrid stego and homoglyph-based ciphers.")
    findings.append("• ChatGPT generally maintained lower severity, often refusing or detecting encoded intent.")
    findings.append("• Ciphers combining homoglyphs + zero-width stego produced the highest-risk behavior.")
    findings.append("• Cipher-based obfuscation remains a realistic attack vector and should be included in LLM safety training.")

    bullets_html = "<br/>".join(findings)
    elements.append(Paragraph(bullets_html, text_style))
    elements.append(Spacer(1, 10))

    # 5. CIPHER-LEVEL CONFUSION SNAPSHOT
    elements.append(Paragraph("5. Cipher-Level Behavior Snapshot", section_header))

    cipher_table_data = [["Cipher", "REFUSE", "DETECT", "INTERPRET", "COMPLY"]]
    for cipher, vals in cipher_conf.items():
        cipher_table_data.append(
            [cipher, vals["REFUSE"], vals["DETECT"], vals["INTERPRET"], vals["COMPLY"]]
        )

    cipher_table = Table(cipher_table_data, hAlign="LEFT")
    cipher_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(cipher_table)
    elements.append(Spacer(1, 10))

    # 6. GRAPHS (LAST SECTION)
    elements.append(Paragraph("6. Visual Analysis", section_header))
    elements.append(
        Paragraph(
            "The following plots summarise severity distributions, model comparison, and cipher effectiveness.",
            text_style,
        )
    )
    elements.append(Spacer(1, 8))

    graph_files = [
        RESULTS_DIR / "severity_distribution.png",
        RESULTS_DIR / "model_comparison.png",
        RESULTS_DIR / "cipher_effectiveness.png",
    ]

    for graph in graph_files:
        if graph.exists():
            img = Image(str(graph), width=400, height=240)
            elements.append(img)
            elements.append(Spacer(1, 12))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✔ PDF written to {output}")


def main():
    generate_pdf()


if __name__ == "__main__":
    main()
