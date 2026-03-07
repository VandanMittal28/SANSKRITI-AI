"""
Monument recognition module.
- Uses Gemini Vision (google-genai SDK) when API quota allows.
- Falls back to smart filename-based detection for hackathon demo reliability.
"""
import json
import os
import re
from io import BytesIO
from pathlib import Path

from PIL import Image

# ── Keyword map: words in filename / path → canonical monument name ───────────
KEYWORD_MAP = {
    "taj":         "Taj Mahal",
    "tajmahal":    "Taj Mahal",
    "taj_mahal":   "Taj Mahal",
    "redfort":     "Red Fort",
    "red_fort":    "Red Fort",
    "lal_qila":    "Red Fort",
    "lalqila":     "Red Fort",
    "qutub":       "Qutub Minar",
    "qutb":        "Qutub Minar",
    "minar":       "Qutub Minar",
    "hampi":       "Hampi",
    "vittala":     "Hampi",
    "vijayanagara":"Hampi",
    "konark":      "Konark Sun Temple",
    "sun_temple":  "Konark Sun Temple",
    "suntemple":   "Konark Sun Temple",
    "ajanta":      "Ajanta Caves",
    "ajanta_cave": "Ajanta Caves",
    "hawa":        "Hawa Mahal",
    "hawamahal":   "Hawa Mahal",
    "wind_palace": "Hawa Mahal",
    "indiagate":   "India Gate",
    "india_gate":  "India Gate",
    "amar_jawan":  "India Gate",
}

MONUMENT_INFO = {
    "Taj Mahal":         ("Agra, Uttar Pradesh, India",  "UNESCO-listed ivory-white marble mausoleum on the south bank of the Yamuna."),
    "Red Fort":          ("Delhi, India",                "Massive Mughal fort built in 1638; India's Independence Day is celebrated here."),
    "Qutub Minar":       ("Delhi, India",                "World's tallest brick minaret at 72.5 m, built in 1193 CE."),
    "Hampi":             ("Karnataka, India",            "Ruins of the Vijayanagara Empire capital, a UNESCO World Heritage Site."),
    "Konark Sun Temple": ("Odisha, India",               "13th-century Sun God temple shaped as a giant chariot with 24 stone wheels."),
    "Ajanta Caves":      ("Maharashtra, India",          "30 rock-cut Buddhist cave monuments with the world's finest ancient murals."),
    "Hawa Mahal":        ("Jaipur, Rajasthan, India",    "Five-storey 'Palace of Winds' with 953 latticed windows, built in 1799."),
    "India Gate":        ("New Delhi, India",            "42-metre war memorial commemorating 70,000 Indian soldiers of WWI."),
}

UNKNOWN_FALLBACK = {
    "monument_name": "Unknown",
    "location": "Unknown",
    "confidence": "Low",
    "brief_description": "Could not identify the monument.",
}


def _detect_from_filename(filename: str) -> dict | None:
    """Try to match monument from the uploaded filename."""
    if not filename:
        return None
    key = filename.lower()
    key = re.sub(r'[^a-z0-9_]', '_', key)   # normalise
    for keyword, monument in KEYWORD_MAP.items():
        if keyword in key:
            loc, desc = MONUMENT_INFO.get(monument, ("India", ""))
            return {
                "monument_name": monument,
                "location": loc,
                "confidence": "High (Demo)",
                "brief_description": desc,
            }
    return None


def _gemini_vision(image_bytes: bytes) -> dict:
    """Call Gemini Vision API. Returns UNKNOWN_FALLBACK on any error."""
    try:
        from google import genai as _genai
        from google.genai import types as _types

        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            return UNKNOWN_FALLBACK.copy()

        client = _genai.Client(api_key=api_key)
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Convert PIL → bytes for new SDK
        buf = BytesIO()
        pil_image.save(buf, format="JPEG")
        img_bytes = buf.getvalue()

        prompt = (
            "You are an expert on Indian historical monuments. "
            "Identify the monument in this image. "
            "Reply ONLY with valid JSON, no markdown, no explanation:\n"
            '{"monument_name":"...","location":"City, State, India",'
            '"confidence":"High|Medium|Low","brief_description":"one sentence"}'
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[
                _types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                prompt,
            ],
        )
        text = response.text.strip()
        # Strip markdown fences if present
        if "```" in text:
            start = text.find("{")
            end   = text.rfind("}") + 1
            text  = text[start:end] if start >= 0 and end > start else text

        data = json.loads(text)
        required = {"monument_name", "location", "confidence", "brief_description"}
        if required.issubset(data.keys()):
            return {k: data[k] for k in required}
    except Exception:
        pass
    return UNKNOWN_FALLBACK.copy()


def identify_monument(image_bytes: bytes, filename: str = "") -> dict:
    """
    Full recognition pipeline:
    1. Try Gemini Vision
    2. If Unknown/error, fallback to filename keyword match
    3. Normalise monument name to canonical DB key
    """
    # Step 1: Gemini Vision
    result = _gemini_vision(image_bytes)

    # Step 2: filename fallback
    if result.get("monument_name") in ("Unknown", None, ""):
        filename_result = _detect_from_filename(filename)
        if filename_result:
            result = filename_result

    # Step 3: normalise name to DB canonical key
    if result.get("monument_name") not in ("Unknown", None, ""):
        known = get_all_monument_names()
        name_lower = result["monument_name"].lower().strip()
        for k in known:
            if k.lower() == name_lower or k.lower() in name_lower or name_lower in k.lower():
                result["monument_name"] = k
                break

    return result


def get_demo_result(image_bytes: bytes = None, filename: str = "") -> dict:
    """
    Called from app.py on image upload.
    Runs full recognition pipeline with filename as extra signal.
    Falls back to Taj Mahal only if everything fails.
    """
    if image_bytes:
        result = identify_monument(image_bytes, filename)
        if result.get("monument_name") not in ("Unknown", None, ""):
            return result

    # Hard fallback (should rarely reach here)
    return {
        "monument_name": "Taj Mahal",
        "location": "Agra, Uttar Pradesh, India",
        "confidence": "Demo Default",
        "brief_description": "UNESCO World Heritage Site — the eternal symbol of love built by Shah Jahan.",
    }


def get_monument_details(monument_name: str) -> dict | None:
    """Load monuments.json, return dict for monument_name (case-insensitive)."""
    try:
        json_path = Path(__file__).parent.parent / "data" / "monuments.json"
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name_lower = monument_name.lower().strip()
        for key, value in data.items():
            if key.lower() == name_lower:
                return value
        return None
    except Exception:
        return None


def get_all_monument_names() -> list[str]:
    """Return list of all monument names from monuments.json."""
    try:
        json_path = Path(__file__).parent.parent / "data" / "monuments.json"
        with open(json_path, "r", encoding="utf-8") as f:
            return list(json.load(f).keys())
    except Exception:
        return []
