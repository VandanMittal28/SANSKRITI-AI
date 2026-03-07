"""
Sustainability and responsible tourism tips module using Gemini API.
"""
import json
import os
from google import genai


def get_sustainability_tips(monument_name: str, monument_details: dict | None) -> dict:
    """
    Get sustainability tips from Gemini API for a specific monument.
    Returns demo tips on error.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or not api_key.strip():
            return get_demo_sustainability_tips(monument_name)

        client = genai.Client(api_key=api_key)

        prompt = f"""You are a sustainable tourism expert for Indian heritage sites.
Generate specific sustainability and responsible tourism tips for visitors to {monument_name}.

Respond in this exact JSON format only, no extra text:
{{
  "environmental_tips": [
    "tip 1",
    "tip 2", 
    "tip 3"
  ],
  "cultural_tips": [
    "tip 1",
    "tip 2",
    "tip 3"
  ],
  "photography_tips": [
    "tip 1",
    "tip 2",
    "tip 3"
  ],
  "conservation_message": "One inspiring sentence about why preserving this monument matters."
}}"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        text = response.text.strip()

        # Extract JSON if wrapped in markdown code block
        if "```" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                text = text[start:end]

        # Normalize single quotes to double quotes for valid JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            text = text.replace("'", '"')
            data = json.loads(text)

        # Validate required keys
        required = {"environmental_tips", "cultural_tips", "photography_tips", "conservation_message"}
        if required.issubset(set(data.keys())):
            return {
                "environmental_tips": data.get("environmental_tips", []),
                "cultural_tips": data.get("cultural_tips", []),
                "photography_tips": data.get("photography_tips", []),
                "conservation_message": data.get("conservation_message", ""),
            }

        return get_demo_sustainability_tips(monument_name)
    except Exception:
        return get_demo_sustainability_tips(monument_name)


def get_demo_sustainability_tips(monument_name: str) -> dict:
    """
    Return hardcoded sustainability tips for demo/fallback mode.
    Works for any monument.
    """
    return {
        "environmental_tips": [
            "Carry a reusable water bottle — plastic bottles are banned near most heritage sites",
            "Use public transport or walk when possible to reduce carbon footprint",
            "Dispose of waste properly in designated bins — never litter on monument grounds",
        ],
        "cultural_tips": [
            "Dress modestly and respectfully — cover shoulders and knees when visiting religious sites",
            "Follow all posted rules and guidelines — monuments are protected cultural heritage",
            "Be quiet and respectful — these are sacred spaces for many visitors",
        ],
        "photography_tips": [
            "Check photography rules — flash photography may be prohibited to protect ancient structures",
            "Respect 'No Photography' zones — some areas are restricted for conservation",
            "Don't touch or lean on monuments — oils from skin can damage delicate surfaces",
        ],
        "conservation_message": f"Preserving {monument_name} ensures future generations can experience India's rich cultural heritage and architectural marvels.",
    }
