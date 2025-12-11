import google.generativeai as genai
from src.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

print("\n=== Models that support generateContent ===")
for m in genai.list_models():
    # Try supported_generation_methods first, then fall back to supported_methods
    supported = getattr(m, "supported_generation_methods", None)
    if not supported:
        supported = getattr(m, "supported_methods", None)
    
    # Get the name
    name = getattr(m, "name", None)
    
    # Check if generateContent is supported
    if supported and "generateContent" in supported:
        print(f"- {name}")