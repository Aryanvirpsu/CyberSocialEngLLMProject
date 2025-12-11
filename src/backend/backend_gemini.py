# src/backend/backend_gemini.py

import google.generativeai as genai
from ..config import GEMINI_API_KEY, GEMINI_MODEL


# Configure Gemini client
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in your .env file")

genai.configure(api_key=GEMINI_API_KEY)


def run_gemini(prompt: str) -> dict:
    """
    Call Gemini and return both raw and cleaned text.

    Returns dict:
    {
        "success": bool,
        "raw": str,
        "clean": str
    }
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        raw_text = getattr(response, "text", None)
        if raw_text is None:
            # Fallback if API structure changes
            raw_text = str(response)

        cleaned_text = raw_text.strip()

        return {
            "success": True,
            "raw": raw_text,
            "clean": cleaned_text,
        }

    except Exception as e:
        err_msg = f"ERROR calling Gemini: {e}"
        return {
            "success": False,
            "raw": err_msg,
            "clean": err_msg,
        }
