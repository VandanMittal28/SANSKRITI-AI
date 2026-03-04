"""
AI Chatbot module for heritage guide using Gemini API.
"""
import os

import google.generativeai as genai


def get_ai_response(
    user_question: str, monument_name: str, monument_details: dict | None, chat_history: list
) -> str:
    """
    Get AI response from Gemini using monument context and chat history.
    Returns error message on failure.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or not api_key.strip():
            return "I apologize, I couldn't process that question. Please try again."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Build context from monument_details
        if monument_details:
            context = f"""
You are Sanskriti AI, an expert heritage guide for Indian monuments.
You are currently answering questions about: {monument_name}

Here is what you know about this monument:
- Built By: {monument_details.get('built_by', 'Unknown')}
- Year Built: {monument_details.get('year_built', 'Unknown')}
- Location: {monument_details.get('location', 'Unknown')}
- Architecture: {monument_details.get('architecture', 'Unknown')}
- Cultural Importance: {monument_details.get('cultural_importance', 'Unknown')}
- Key Facts: {', '.join(monument_details.get('key_facts', []))}
- Fun Fact: {monument_details.get('fun_fact', 'Unknown')}
- Best Time to Visit: {monument_details.get('best_time_to_visit', 'Unknown')}
- Entry Fee: {monument_details.get('entry_fee', 'Unknown')}

Answer questions in a friendly, informative, and engaging way.
Keep responses concise (2-4 sentences max unless more detail is needed).
If asked something outside your knowledge of this monument, politely say so.
Always stay in character as a heritage guide.
"""
        else:
            context = f"""
You are Sanskriti AI, an expert heritage guide for Indian monuments.
You are currently answering questions about: {monument_name}

Answer questions in a friendly, informative, and engaging way.
Keep responses concise (2-4 sentences max unless more detail is needed).
If asked something outside your knowledge of this monument, politely say so.
Always stay in character as a heritage guide.
"""

        # Build conversation history string
        conversation = ""
        for msg in chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                conversation += f"User: {content}\n"
            elif role == "assistant":
                conversation += f"Assistant: {content}\n"

        # Combine context, history, and current question
        full_prompt = f"{context}\n\n{conversation}User: {user_question}\nAssistant:"

        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception:
        return "I apologize, I couldn't process that question. Please try again."


def get_demo_response(user_question: str, monument_name: str) -> str:
    """
    Return hardcoded demo responses for common questions.
    Uses monument_name to provide basic info.
    """
    question_lower = user_question.lower()

    # Get monument details for demo responses
    from modules.recognition import get_monument_details

    details = get_monument_details(monument_name)

    if not details:
        return f"Great question about {monument_name}! This monument is one of India's most treasured heritage sites. Ask me about its history, architecture, or visitor information!"

    if "who built" in question_lower or "built by" in question_lower:
        return f"{monument_name} was built by {details.get('built_by', 'Unknown')}. {details.get('cultural_importance', '')[:100]}..."

    if "when" in question_lower or "year" in question_lower:
        return f"{monument_name} was built between {details.get('year_built', 'Unknown')}. It's a remarkable example of {details.get('type', 'heritage site')} architecture."

    if "where" in question_lower or "location" in question_lower:
        return f"{monument_name} is located in {details.get('location', 'Unknown')}. It's easily accessible and a must-visit destination for heritage enthusiasts!"

    if "architecture" in question_lower or "style" in question_lower:
        return f"{monument_name} features {details.get('architecture', 'remarkable architecture')[:150]}..."

    if "entry" in question_lower or "fee" in question_lower or "ticket" in question_lower:
        return f"The entry fee for {monument_name} is {details.get('entry_fee', 'varies')}. {details.get('best_time_to_visit', '')} is the best time to visit!"

    if "best time" in question_lower or "visit" in question_lower or "when to" in question_lower:
        return f"The best time to visit {monument_name} is {details.get('best_time_to_visit', 'during cooler months')}. The entry fee is {details.get('entry_fee', 'reasonable')}."

    return f"Great question about {monument_name}! This monument is one of India's most treasured heritage sites. Ask me about its history, architecture, or visitor information!"
