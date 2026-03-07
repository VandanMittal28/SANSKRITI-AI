from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

from modules.chatbot import get_ai_response, get_demo_response
from modules.quiz import get_quiz_questions
from modules.recognition import get_all_monument_names, get_demo_result, get_monument_details, identify_monument
from modules.sustainability import get_demo_sustainability_tips, get_sustainability_tips
<<<<<<< HEAD
from modules.gamification.dashboard import render_dashboard
from modules.gamification.xp_system import award_xp as gamification_award_xp
from modules.gamification.achievements import check_and_award_badges as gamification_check_and_award_badges
from modules.gamification.hidden_gems import check_nearby_gems, show_gem_unlock_ui
=======
>>>>>>> 07dc145c19582e5525ab4c2d7040077e47ce921b

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Sanskriti AI", page_icon="🏛️", layout="wide")

# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "monument_result" not in st.session_state:
    st.session_state["monument_result"] = None
if "monument_details" not in st.session_state:
    st.session_state["monument_details"] = None
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = None
if "current_question_index" not in st.session_state:
    st.session_state["current_question_index"] = 0
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = []
if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False
if "quiz_completed" not in st.session_state:
    st.session_state["quiz_completed"] = False

# ── Gamification / XP ─────────────────────────────────────────────────────────
if "xp" not in st.session_state:
    st.session_state["xp"] = 0
if "achievements" not in st.session_state:
    st.session_state["achievements"] = set()
if "monuments_visited" not in st.session_state:
    st.session_state["monuments_visited"] = set()
if "quizzes_completed" not in st.session_state:
    st.session_state["quizzes_completed"] = 0
if "xp_log" not in st.session_state:
    st.session_state["xp_log"] = []
if "_last_uploaded_name" not in st.session_state:
    st.session_state["_last_uploaded_name"] = None
if "_manual_select_value" not in st.session_state:
    st.session_state["_manual_select_value"] = "— Select from list —"
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "page_id" not in st.session_state:
    st.session_state["page_id"] = "home"


# ─────────────────────────────────────────────────────────────────────────────
# Translations (English / Hindi)
# ─────────────────────────────────────────────────────────────────────────────
TRANSLATIONS = {
    # Page names
    "page_home":           {"en": "🏠 Home",                  "hi": "🏠 होम"},
    "page_recognition":    {"en": "🔍 Monument Recognition",  "hi": "🔍 स्मारक पहचान"},
    "page_chatbot":        {"en": "🤖 AI Chatbot",            "hi": "🤖 AI चैटबॉट"},
    "page_sustainability": {"en": "🌿 Sustainability",        "hi": "🌿 संधारणीयता"},
    "page_quiz":           {"en": "🧠 Quiz",                  "hi": "🧠 क्विज़"},
    "page_achievements":   {"en": "🏅 Achievements",          "hi": "🏅 उपलब्धियाँ"},

    # Sidebar
    "sidebar_title":       {"en": "🏛️ Sanskriti",             "hi": "🏛️ संस्कृति"},
    "sidebar_subtitle":    {"en": "AI Heritage Guide",        "hi": "AI विरासत गाइड"},
    "explorer_progress":   {"en": "🎮 Explorer Progress",     "hi": "🎮 एक्सप्लोरर प्रगति"},
    "badges":              {"en": "🏅 Badges",                "hi": "🏅 बैज"},
    "demo_flow":           {"en": "🎬 Demo Flow",             "hi": "🎬 डेमो फ़्लो"},
    "max_level":           {"en": "Max level reached! 🎉",    "hi": "अधिकतम स्तर! 🎉"},
    "xp_to_next":          {"en": "XP to next level",         "hi": "XP अगले स्तर तक"},
    "lang_toggle":         {"en": "🇮🇳 हिंदी में देखें",        "hi": "🇬🇧 Switch to English"},

    # Home
    "hero_badge":          {"en": "✦ AI-Powered Heritage Guide", "hi": "✦ AI-संचालित विरासत गाइड"},
    "hero_title_1":        {"en": "Discover India's",            "hi": "भारत की"},
    "hero_title_2":        {"en": "Living Heritage",             "hi": "जीवित विरासत खोजें"},
    "hero_desc":           {"en": "Upload a monument photograph and let AI guide you through 5,000 years of history, culture, and architecture.",
                            "hi": "एक स्मारक की तस्वीर अपलोड करें और AI को 5,000 साल के इतिहास, संस्कृति और वास्तुकला की गाइड बनने दें।"},
    "monuments_covered":   {"en": "Monuments Covered",   "hi": "स्मारक शामिल"},
    "ai_powered":          {"en": "AI Powered",          "hi": "AI संचालित"},
    "sdg_aligned":         {"en": "SDG Aligned",         "hi": "SDG संरेखित"},
    "response_time":       {"en": "Response Time",       "hi": "प्रतिक्रिया समय"},
    "smart_recognition":   {"en": "🔍 Smart Recognition",    "hi": "🔍 स्मार्ट पहचान"},
    "smart_recognition_d": {"en": "Upload any monument photo for instant AI identification",
                            "hi": "किसी भी स्मारक की तस्वीर अपलोड करें तुरंत AI पहचान के लिए"},
    "heritage_chatbot":    {"en": "🤖 Heritage Chatbot",      "hi": "🤖 विरासत चैटबॉट"},
    "heritage_chatbot_d":  {"en": "Ask anything about history, architecture, culture",
                            "hi": "इतिहास, वास्तुकला, संस्कृति के बारे में कुछ भी पूछें"},
    "sustainability_guide":{"en": "🌿 Sustainability Guide",  "hi": "🌿 संधारणीयता गाइड"},
    "sustainability_guide_d":{"en": "SDG-aligned responsible tourism tips",
                              "hi": "SDG-संरेखित जिम्मेदार पर्यटन सुझाव"},
    "knowledge_quiz":      {"en": "🧠 Knowledge Quiz",        "hi": "🧠 ज्ञान क्विज़"},
    "knowledge_quiz_d":    {"en": "Test your heritage knowledge with AI-generated MCQs",
                            "hi": "AI-जनित MCQ से अपने विरासत ज्ञान की परीक्षा लें"},
    "how_to_use":          {"en": "🚀 How to use Sanskriti AI", "hi": "🚀 संस्कृति AI कैसे उपयोग करें"},
    "tech_stack":          {"en": "🛠️ Tech Stack",            "hi": "🛠️ टेक स्टैक"},
    "problem_solved":      {"en": "🎯 Problem Solved",        "hi": "🎯 समस्या हल"},
    "impact":              {"en": "🌍 Impact",                "hi": "🌍 प्रभाव"},

    # Recognition
    "monument_recognition":    {"en": "Monument Recognition",          "hi": "स्मारक पहचान"},
    "select_monument":         {"en": "🗺️ Select a monument to explore (or upload an image below):",
                                "hi": "🗺️ एक स्मारक चुनें (या नीचे छवि अपलोड करें):"},
    "select_placeholder":      {"en": "— Select a monument —",        "hi": "— एक स्मारक चुनें —"},
    "upload_label":            {"en": "📸 Or upload a monument photo for AI identification:",
                                "hi": "📸 या AI पहचान के लिए स्मारक फ़ोटो अपलोड करें:"},
    "identifying":             {"en": "🔍 Identifying monument with AI Vision...",
                                "hi": "🔍 AI विज़न से स्मारक की पहचान हो रही है..."},
    "manually_selected":       {"en": "📖 Manually selected",          "hi": "📖 मैन्युअल रूप से चयनित"},
    "monument_identified":     {"en": "✅ Monument Identified!",       "hi": "✅ स्मारक पहचाना गया!"},
    "detailed_info":           {"en": "📚 Detailed Information",       "hi": "📚 विस्तृत जानकारी"},
    "tab_history":             {"en": "📖 History",                    "hi": "📖 इतिहास"},
    "tab_architecture":        {"en": "🏛️ Architecture",              "hi": "🏛️ वास्तुकला"},
    "tab_facts":               {"en": "📊 Key Facts",                 "hi": "📊 मुख्य तथ्य"},
    "tab_fun":                 {"en": "💡 Fun Facts",                 "hi": "💡 रोचक तथ्य"},
    "tab_visitor":             {"en": "🎯 Visitor Info",              "hi": "🎯 दर्शक जानकारी"},
    "share_exploration":       {"en": "📲 Share Your Exploration",     "hi": "📲 अपनी खोज साझा करें"},
    "copy_share":              {"en": "Copy & share on social media:", "hi": "कॉपी करें और सोशल मीडिया पर साझा करें:"},
    "go_to_quiz":              {"en": "Go to Quiz →",                 "hi": "क्विज़ पर जाएं →"},
    "upload_or_select":        {"en": "📸 Upload a monument image above, or select one from the dropdown to begin",
                                "hi": "📸 ऊपर एक स्मारक छवि अपलोड करें, या ड्रॉपडाउन से चुनें"},

    # Chatbot
    "ai_chatbot":              {"en": "🤖 AI Heritage Chatbot",       "hi": "🤖 AI विरासत चैटबॉट"},
    "chatting_about":          {"en": "🏛️ Chatting about",            "hi": "🏛️ बातचीत हो रही है"},
    "ask_anything":            {"en": "Ask anything about",           "hi": "कुछ भी पूछें"},
    "thinking":                {"en": "🤔 Thinking...",               "hi": "🤔 सोच रहा हूँ..."},
    "clear_chat":              {"en": "🗑️ Clear Chat",                "hi": "🗑️ चैट साफ़ करें"},

    # Sustainability
    "sustainable_tourism":     {"en": "Sustainable & Responsible Tourism", "hi": "संधारणीय और जिम्मेदार पर्यटन"},
    "sustainability_tips_for": {"en": "🌿 Sustainability tips for",       "hi": "🌿 संधारणीयता सुझाव"},
    "environmental_tips":      {"en": "🌱 Environmental Tips",            "hi": "🌱 पर्यावरण सुझाव"},
    "cultural_respect":        {"en": "🏛️ Cultural Respect",             "hi": "🏛️ सांस्कृतिक सम्मान"},
    "responsible_photo":       {"en": "📸 Responsible Photography",       "hi": "📸 जिम्मेदार फ़ोटोग्राफ़ी"},

    # Quiz
    "heritage_quiz":           {"en": "🧠 Heritage Knowledge Quiz",    "hi": "🧠 विरासत ज्ञान क्विज़"},
    "quiz_about":              {"en": "🏛️ Quiz about",                 "hi": "🏛️ क्विज़ विषय"},
    "start_quiz":              {"en": "🚀 Start Quiz",                 "hi": "🚀 क्विज़ शुरू करें"},
    "submit_answer":           {"en": "✅ Submit Answer",              "hi": "✅ उत्तर जमा करें"},
    "quiz_completed":          {"en": "🎉 Quiz Completed!",           "hi": "🎉 क्विज़ पूरा हुआ!"},
    "retake_quiz":             {"en": "🔄 Retake Quiz",               "hi": "🔄 दोबारा दें"},
    "review_answers":          {"en": "📋 Review Your Answers:",       "hi": "📋 अपने उत्तर देखें:"},
    "share_achievement":       {"en": "📲 Share Your Achievement",     "hi": "📲 अपनी उपलब्धि साझा करें"},

    # Achievements
    "achievements_title":      {"en": "🏅 Achievements & Explorer Progress", "hi": "🏅 उपलब्धियाँ और एक्सप्लोरर प्रगति"},
    "current_level":           {"en": "Current Level",                "hi": "वर्तमान स्तर"},
    "xp_earned":               {"en": "XP earned",                    "hi": "XP अर्जित"},
    "badge_collection":        {"en": "🏅 Badge Collection",          "hi": "🏅 बैज संग्रह"},
    "monuments_explored":      {"en": "🗺️ Monuments Explored",       "hi": "🗺️ खोजे गए स्मारक"},
    "xp_activity_log":         {"en": "⚡ XP Activity Log",           "hi": "⚡ XP गतिविधि लॉग"},
    "unlocked":                {"en": "✅ Unlocked",                  "hi": "✅ अनलॉक"},
    "no_monuments_yet":        {"en": "🏛️ You haven't explored any monuments yet — go to **Monument Recognition** to start!",
                                "hi": "🏛️ आपने अभी तक कोई स्मारक नहीं खोजा — **स्मारक पहचान** पर जाएं!"},

    # Footer
    "footer_left":            {"en": "SANSKRITI AI © 2025",           "hi": "संस्कृति AI © 2025"},
    "footer_right":           {"en": "BUILT WITH ♥ FOR INDIA'S HERITAGE",
                               "hi": "भारत की विरासत के लिए ♥ से बनाया गया"},
}

# Page ID → translation key mapping
PAGE_IDS = ["home", "recognition", "chatbot", "sustainability", "quiz", "achievements"]
PAGE_KEYS = ["page_home", "page_recognition", "page_chatbot", "page_sustainability", "page_quiz", "page_achievements"]


def T(key: str) -> str:
    """Return translated string for the current language."""
    lang = st.session_state.get("lang", "en")
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))


XP_RULES = {
    "view_monument": 10,
    "complete_quiz": 20,
    "ask_chatbot": 5,
}

LEVELS = [
    (0,   "🌱 Beginner Explorer"),
    (50,  "🏛️ Heritage Explorer"),
    (150, "🎓 Cultural Pro"),
    (300, "👑 Sanskriti Legend"),
]

BADGES = {
    "first_visit":       ("🏆", "First Monument Visited",    "Explored your first monument"),
    "quiz_master":       ("🧠", "Quiz Master",               "Completed 2 quizzes"),
    "heritage_champion": ("🌟", "Heritage Champion",         "Earned 150+ XP"),
}


def award_xp(reason: str) -> int:
    """Add XP for the given reason key, check achievements, return points earned."""
    points = XP_RULES.get(reason, 0)
    st.session_state["xp"] += points
    st.session_state["xp_log"].append(f"+{points} XP — {reason.replace('_', ' ').title()}")
<<<<<<< HEAD
    
    # Sync Gamification System
    gamification_award_xp("demo_user", points)
    
=======
>>>>>>> 07dc145c19582e5525ab4c2d7040077e47ce921b
    _check_achievements()
    return points


def _check_achievements():
    xp    = st.session_state["xp"]
    ach   = st.session_state["achievements"]
    vis   = st.session_state["monuments_visited"]
    quizz = st.session_state["quizzes_completed"]

    if vis and "first_visit" not in ach:
        ach.add("first_visit")
        st.toast("🏆 Achievement Unlocked: First Monument Visited!", icon="🏆")
    if quizz >= 2 and "quiz_master" not in ach:
        ach.add("quiz_master")
        st.toast("🧠 Achievement Unlocked: Quiz Master!", icon="🧠")
    if xp >= 150 and "heritage_champion" not in ach:
        ach.add("heritage_champion")
        st.toast("🌟 Achievement Unlocked: Heritage Champion!", icon="🌟")

    st.session_state["achievements"] = ach
<<<<<<< HEAD
    
    # Sync Gamification System Badges
    new_badges = gamification_check_and_award_badges("demo_user", xp, len(vis), quizz > 0)
    for badge in new_badges:
        st.toast(f"{badge['icon']} New Badge Unlocked: {badge['title']}", icon=badge['icon'])
=======
>>>>>>> 07dc145c19582e5525ab4c2d7040077e47ce921b


def get_level(xp: int) -> str:
    level = LEVELS[0][1]
    for threshold, label in LEVELS:
        if xp >= threshold:
            level = label
    return level


def get_next_level_xp(xp: int) -> int | None:
    for threshold, _ in LEVELS:
        if xp < threshold:
            return threshold
    return None


def generate_caption(monument_name: str) -> str:
    """Generate a shareable social media caption for a monument."""
    return (
        f"🏛️ Just explored {monument_name} with Sanskriti AI!\n"
        f"Discovering India's heritage through AI-powered storytelling.\n"
        f"#SanskritiAI #HeritageExplorer #IncredibleIndia #{monument_name.replace(' ', '')}"
    )

<<<<<<< HEAD
=======

def render_voice_guide(monument_name: str) -> None:
    """Render a voice guide section for listening to monument narration.

    The function displays a simple interface to select a language and play 
    the corresponding audio file. Audio files follow the naming pattern:
    {monument_name_lowercase_with_underscores}_{language_code}.mp3

    Args:
        monument_name: The name of the monument (e.g., "Taj Mahal").
    """
    # Reset per‑monument state when name changes
    prev = st.session_state.get("last_voice_monument")
    if prev != monument_name:
        for key in list(st.session_state.keys()):
            if key.startswith("voice_clicked_") or key.startswith("voice_lang_"):
                st.session_state.pop(key, None)
        st.session_state["last_voice_monument"] = monument_name

    with st.container():
        st.markdown("## 🎧 Voice Guide")
        clicked = st.button("Listen to Emperor", key=f"listen_{monument_name}")
        if clicked:
            st.session_state[f"voice_clicked_{monument_name}"] = True

        if st.session_state.get(f"voice_clicked_{monument_name}", False):
            lang = st.radio("Language", ["English", "Hindi"], key=f"voice_lang_{monument_name}")

            # Convert monument name to file format: lowercase, replace spaces with underscores
            clean_name = monument_name.lower().strip().replace(" ", "_")
            
            # Determine language suffix
            lang_suffix = "en" if lang == "English" else "hi"
            
            # Build absolute path to audio file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            audio_file = os.path.join(base_dir, "assets", "audio", f"{clean_name}_{lang_suffix}.mp3")
            
            # Display the file path being searched for (debug)
            st.write(f"Looking for: `{clean_name}_{lang_suffix}.mp3`")
            
            # Check if file exists and play it
            if os.path.exists(audio_file):
                st.audio(audio_file)
            else:
                st.error(f"Audio file not found: {clean_name}_{lang_suffix}.mp3")

>>>>>>> 07dc145c19582e5525ab4c2d7040077e47ce921b
# -----------------------------------------------------------------------------
# Custom CSS — Indian Heritage Theme
# -----------------------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Philosopher:wght@400;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --saffron: #D4893F;
  --saffron-light: #E8A85C;
  --saffron-dim: rgba(212, 137, 63, 0.12);
  --gold: #C9A84C;
  --gold-light: #E8C97A;
  --gold-dim: rgba(201, 168, 76, 0.12);
  --terracotta: #C45B3A;
  --maroon: #7A2E3B;
  --deep-indigo: #1B1040;
  --temple-dark: #120E24;
  --bg-primary: #0F0B1E;
  --bg-secondary: #161230;
  --bg-card: rgba(28, 22, 56, 0.85);
  --bg-card-hover: rgba(35, 28, 68, 0.95);
  --border: rgba(201, 168, 76, 0.2);
  --border-strong: rgba(212, 137, 63, 0.5);
  --text-primary: #F5E6D3;
  --text-secondary: #C4A882;
  --text-muted: #8A7560;
  --accent-teal: #4B9B8E;
  --success: #4B8E6E;
  --radius: 14px;
  --radius-lg: 22px;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: linear-gradient(170deg, #0F0B1E 0%, #1B1040 30%, #1A0E30 60%, #120E24 100%) !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-primary) !important;
}

/* Subtle mandala watermark */
.stApp::before {
  content: '';
  position: fixed;
  top: -20%; right: -15%;
  width: 900px; height: 900px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ccircle cx='100' cy='100' r='90' fill='none' stroke='%23C9A84C' stroke-width='0.3' opacity='0.08'/%3E%3Ccircle cx='100' cy='100' r='70' fill='none' stroke='%23C9A84C' stroke-width='0.3' opacity='0.06'/%3E%3Ccircle cx='100' cy='100' r='50' fill='none' stroke='%23C9A84C' stroke-width='0.3' opacity='0.05'/%3E%3Ccircle cx='100' cy='100' r='30' fill='none' stroke='%23D4893F' stroke-width='0.4' opacity='0.06'/%3E%3Cpath d='M100 10 L100 190 M10 100 L190 100 M29 29 L171 171 M171 29 L29 171' stroke='%23C9A84C' stroke-width='0.2' opacity='0.04'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  pointer-events: none;
  z-index: 0;
  animation: floatMandala 60s ease-in-out infinite;
}

/* Grain overlay */
.stApp::after {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
  opacity: 0.3;
}

@keyframes floatMandala {
  0%, 100% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(15deg) scale(1.05); }
}

.main .block-container {
  padding: 2rem 3rem 4rem 3rem !important;
  max-width: 1200px !important;
}

/* ── Sidebar — Temple corridor feel ──────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0D0820 0%, #130E28 50%, #0D0820 100%) !important;
  border-right: 1px solid rgba(201,168,76,0.15) !important;
  box-shadow: 4px 0 30px rgba(0,0,0,0.4) !important;
}

[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--saffron), var(--gold), var(--saffron), transparent);
}

[data-testid="stSidebar"] > div { padding: 2rem 1.2rem !important; }

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: 'Cinzel', serif !important;
  color: var(--gold) !important;
  letter-spacing: 0.05em !important;
}

[data-testid="stSidebar"] .stRadio > label {
  color: var(--text-secondary) !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.92rem !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.02em !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius: 10px !important;
  padding: 0.55rem 0.8rem !important;
  margin: 3px 0 !important;
  transition: all 0.3s ease !important;
  border: 1px solid transparent !important;
  position: relative !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: linear-gradient(135deg, rgba(212,137,63,0.08), rgba(201,168,76,0.08)) !important;
  border-color: rgba(201,168,76,0.2) !important;
}

[data-testid="stSidebar"] .stCaption {
  color: var(--text-muted) !important;
  font-size: 0.75rem !important;
}

[data-testid="stSidebar"] hr {
  border-color: rgba(201,168,76,0.12) !important;
  margin: 1rem 0 !important;
}

/* ── Headings — Cinzel for heritage grandeur ─────────────────────────────── */
h1 {
  font-family: 'Cinzel', serif !important;
  font-size: 2.8rem !important;
  font-weight: 600 !important;
  color: var(--gold) !important;
  letter-spacing: 0.02em !important;
  line-height: 1.15 !important;
  margin-bottom: 0.5rem !important;
}

h2 {
  font-family: 'Cinzel', serif !important;
  font-size: 1.9rem !important;
  font-weight: 500 !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.02em !important;
}

h3 {
  font-family: 'Philosopher', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
  color: var(--saffron-light) !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}

p, .stMarkdown p {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-secondary) !important;
  line-height: 1.75 !important;
  font-size: 0.95rem !important;
}

/* ── Alerts ──────────────────────────────────────────────────────────────── */
.stAlert {
  border-radius: var(--radius) !important;
  border: 1px solid !important;
  backdrop-filter: blur(12px) !important;
}

div[class*="stInfo"] {
  background: rgba(75, 155, 142, 0.08) !important;
  border-color: rgba(75, 155, 142, 0.3) !important;
  color: #7ECDC0 !important;
}

div[class*="stSuccess"] {
  background: rgba(75, 142, 110, 0.08) !important;
  border-color: rgba(75, 142, 110, 0.3) !important;
  color: #7ECDA0 !important;
}

div[class*="stWarning"] {
  background: rgba(212, 137, 63, 0.1) !important;
  border-color: rgba(212, 137, 63, 0.35) !important;
  color: var(--saffron-light) !important;
}

div[class*="stError"] {
  background: rgba(196, 75, 75, 0.08) !important;
  border-color: rgba(196, 75, 75, 0.3) !important;
  color: #E08080 !important;
}

/* ── Buttons — Saffron & Gold ────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--saffron) 0%, var(--gold) 50%, var(--saffron) 100%) !important;
  background-size: 200% 100% !important;
  color: #0A0A0F !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Philosopher', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  padding: 0.65rem 1.5rem !important;
  transition: all 0.35s ease !important;
  box-shadow: 0 4px 24px rgba(212, 137, 63, 0.3) !important;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 35px rgba(212, 137, 63, 0.45) !important;
  background-position: 100% 0 !important;
}

.stButton > button:active { transform: translateY(0px) !important; }

.stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--accent-teal) 0%, #2D6B61 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Philosopher', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  font-size: 0.88rem !important;
  padding: 0.65rem 1.5rem !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 20px rgba(75, 155, 142, 0.25) !important;
}

.stFormSubmitButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(75, 155, 142, 0.4) !important;
}

/* ── File Uploader ───────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 2px dashed var(--border-strong) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.5rem !important;
  transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--saffron) !important;
  background: var(--saffron-dim) !important;
}

[data-testid="stFileUploader"] label {
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── Metrics — with warm glow ────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1.2rem 1.5rem !important;
  transition: all 0.3s ease !important;
  backdrop-filter: blur(10px) !important;
}

[data-testid="stMetric"]:hover {
  border-color: var(--saffron) !important;
  background: var(--bg-card-hover) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 10px 35px rgba(212, 137, 63, 0.12) !important;
}

[data-testid="stMetricLabel"] {
  color: var(--text-muted) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
  font-family: 'Cinzel', serif !important;
  font-size: 1.8rem !important;
  color: var(--gold) !important;
  font-weight: 600 !important;
}

[data-testid="stMetricDelta"] {
  color: var(--text-muted) !important;
  font-size: 0.78rem !important;
}

/* ── Tabs — temple arch style ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 4px !important;
  border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-muted) !important;
  border-radius: 10px !important;
  font-family: 'Philosopher', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.03em !important;
  border: none !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(212,137,63,0.15), rgba(201,168,76,0.1)) !important;
  color: var(--saffron-light) !important;
  border: 1px solid rgba(212,137,63,0.3) !important;
}

.stTabs [data-baseweb="tab"]:hover { color: var(--text-primary) !important; }

.stTabs [data-baseweb="tab-panel"] {
  background: var(--bg-card) !important;
  border-radius: 0 0 var(--radius) var(--radius) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  padding: 1.5rem !important;
  animation: fadeSlideUp 0.4s ease forwards;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Chat ────────────────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem 1.2rem !important;
  margin: 0.5rem 0 !important;
}

.stChatInput textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

.stChatInput textarea:focus {
  border-color: var(--saffron) !important;
  box-shadow: 0 0 0 2px var(--saffron-dim) !important;
}

/* ── Radio, Progress ─────────────────────────────────────────────────────── */
.stRadio div[role="radiogroup"] label {
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.92rem !important;
}

.stProgress > div > div {
  background: linear-gradient(90deg, var(--saffron) 0%, var(--gold-light) 50%, var(--saffron-light) 100%) !important;
  border-radius: 999px !important;
}

.stProgress > div {
  background: var(--bg-card) !important;
  border-radius: 999px !important;
  border: 1px solid var(--border) !important;
}

/* ── Expander ────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-primary) !important;
  font-family: 'Philosopher', sans-serif !important;
  font-weight: 700 !important;
  transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
  border-color: var(--saffron) !important;
  color: var(--saffron-light) !important;
}

.streamlit-expanderContent {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  border-radius: 0 0 var(--radius) var(--radius) !important;
}

/* ── Misc ────────────────────────────────────────────────────────────────── */
hr {
  border-color: var(--border) !important;
  margin: 2rem 0 !important;
}

[data-testid="stImage"] img {
  border-radius: var(--radius-lg) !important;
  border: 1px solid rgba(201,168,76,0.25) !important;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(212,137,63,0.06) !important;
}

.stSpinner > div { border-top-color: var(--saffron) !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(212,137,63,0.4); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--saffron); }

.stCaption, [data-testid="stCaptionContainer"] {
  color: var(--text-muted) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.04em !important;
}

footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] {
  background: rgba(15, 11, 30, 0.9) !important;
  backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(201,168,76,0.12) !important;
}

/* ── Heritage card with decorative corner ────────────────────────────────── */
.heritage-card {
  background: linear-gradient(145deg, rgba(28,22,56,0.9), rgba(22,18,48,0.85));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.8rem;
  transition: all 0.35s ease;
  height: 100%;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.heritage-card::before {
  content: '❖';
  position: absolute;
  top: 10px; right: 14px;
  font-size: 1.1rem;
  color: rgba(212,137,63,0.2);
  transition: color 0.3s ease;
}

.heritage-card:hover {
  border-color: var(--saffron);
  transform: translateY(-5px);
  box-shadow: 0 15px 45px rgba(212, 137, 63, 0.12), 0 0 20px rgba(201,168,76,0.05);
}

.heritage-card:hover::before {
  color: rgba(212,137,63,0.5);
}

/* ── Cultural quote banner ───────────────────────────────────────────────── */
.culture-banner {
  background: linear-gradient(135deg, rgba(212,137,63,0.08), rgba(122,46,59,0.08), rgba(27,16,64,0.3));
  border: 1px solid rgba(212,137,63,0.2);
  border-radius: 16px;
  padding: 1.8rem 2.2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin: 1rem 0;
}

.culture-banner::before,
.culture-banner::after {
  content: '✦';
  position: absolute;
  color: rgba(201,168,76,0.15);
  font-size: 3rem;
}
.culture-banner::before { top: -5px; left: 15px; }
.culture-banner::after { bottom: -5px; right: 15px; }

/* ── Ornamental divider ──────────────────────────────────────────────────── */
.ornament-divider {
  text-align: center;
  margin: 2rem 0;
  color: rgba(201,168,76,0.3);
  font-size: 1rem;
  letter-spacing: 0.5em;
}

/* ── Value pill ──────────────────────────────────────────────────────────── */
.value-pill {
  display: inline-block;
  background: rgba(212,137,63,0.1);
  border: 1px solid rgba(212,137,63,0.25);
  border-radius: 999px;
  padding: 0.3rem 1rem;
  font-size: 0.78rem;
  color: var(--saffron-light);
  font-family: 'Philosopher', sans-serif;
  font-weight: 700;
  letter-spacing: 0.06em;
  margin: 0.2rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .main .block-container {
    padding: 1rem 1rem 3rem 1rem !important;
  }
  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.4rem !important; }
  [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Demo mode — always ON
# -----------------------------------------------------------------------------
demo_mode = True

# -----------------------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    # ── Language toggle ─────────────────────────────────────────────────────
    def _toggle_lang():
        st.session_state["lang"] = "hi" if st.session_state["lang"] == "en" else "en"

    st.button(T("lang_toggle"), on_click=_toggle_lang, key="lang_btn", use_container_width=True)
    st.markdown("")

    st.markdown(f"""
<div style="padding: 0.5rem 0 1.5rem 0; text-align:center;">
  <div style="font-size:1.8rem; margin-bottom:0.3rem;">🕉️</div>
  <div style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:600; color:#D4893F; letter-spacing:0.06em;">
    {T("sidebar_title")}
  </div>
  <div style="font-family:'Philosopher',sans-serif; font-size:0.68rem; color:#8A7560; letter-spacing:0.15em; text-transform:uppercase; margin-top:4px; font-weight:700;">
    {T("sidebar_subtitle")}
  </div>
  <div style="margin-top:0.7rem; color:rgba(201,168,76,0.25); font-size:0.7rem; letter-spacing:0.4em;">✦ ── ✦</div>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    # Build page options from translations (language-aware labels)
    page_options = [T(pk) for pk in PAGE_KEYS]
    current_pid  = st.session_state.get("page_id", "home")
    try:
        default_index = PAGE_IDS.index(current_pid)
    except ValueError:
        default_index = 0

    selected_label = st.radio(
        "Navigate",
        options=page_options,
        index=default_index,
        key="nav_radio",
        label_visibility="collapsed",
    )
    # Map selected label back to page_id
    try:
        sel_idx = page_options.index(selected_label)
    except ValueError:
        sel_idx = 0
    st.session_state["page_id"] = PAGE_IDS[sel_idx]

    st.markdown("---")

    # ── XP & Level display ──────────────────────────────────────────────────
    xp    = st.session_state["xp"]
    level = get_level(xp)
    next_xp = get_next_level_xp(xp)
    st.markdown(f"### {T('explorer_progress')}")
    st.markdown(f"**{level}**")
    st.markdown(f"⚡ **{xp} XP**")
    if next_xp:
        progress_val = min(xp / next_xp, 1.0)
        st.progress(progress_val)
        st.caption(f"{xp} / {next_xp} {T('xp_to_next')}")
    else:
        st.progress(1.0)
        st.caption(T("max_level"))

    # ── Achievement badges in sidebar ────────────────────────────────────────
    earned = st.session_state["achievements"]
    st.markdown(f"**{T('badges')}**")
    for key, (icon, name, desc) in BADGES.items():
        if key in earned:
            st.markdown(
                f"""<div style="background:rgba(201,168,76,0.12);border:1px solid rgba(201,168,76,0.5);
                border-radius:8px;padding:0.5rem 0.7rem;margin:4px 0;display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:1.2rem;">{icon}</span>
                <div><div style="color:#E8C97A;font-size:0.82rem;font-weight:600;">{name}</div>
                <div style="color:#7A6E5C;font-size:0.7rem;">{desc}</div></div></div>""",
                unsafe_allow_html=True,
            )
        else:
            SIDEBAR_UNLOCK_HINTS = {
                "first_visit":       "Visit any monument",
                "quiz_master":       "Complete 2 quizzes",
                "heritage_champion": "Earn 150+ XP",
            }
            st.markdown(
                f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                border-radius:8px;padding:0.5rem 0.7rem;margin:4px 0;display:flex;align-items:center;gap:0.5rem;
                opacity:0.45;">
                <span style="font-size:1.2rem;">🔒</span>
                <div><div style="color:#7A6E5C;font-size:0.82rem;font-weight:600;">{name}</div>
                <div style="color:#5C5445;font-size:0.7rem;">{SIDEBAR_UNLOCK_HINTS.get(key,'')}</div></div></div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(f"### {T('demo_flow')}")
    st.markdown("""
1. 📸 Upload monument image  
2. 🔍 View AI recognition  
3. 📖 Explore history tabs  
4. 🤖 Chat with AI guide  
5. 🌿 Check sustainability  
6. 🧠 Take the quiz  
""")
    st.divider()
    st.caption(T("footer_left"))

# Resolve page_id for routing
active_page = st.session_state.get("page_id", "home")

# -----------------------------------------------------------------------------
# Home page
# -----------------------------------------------------------------------------
if active_page == "home":

    # ── Sanskrit quote banner ─────────────────────────────────────────────────
    st.markdown("""
<div class="culture-banner">
  <div style="font-family:'Cinzel',serif; font-size:1.4rem; color:#E8C97A; font-weight:500; margin-bottom:0.6rem; letter-spacing:0.04em;">
    "वसुधैव कुटुम्बकम्"
  </div>
  <div style="font-family:'Philosopher',sans-serif; font-size:0.85rem; color:#C4A882; font-style:italic;">
    "The World is One Family" — Maha Upanishad
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("")

    # ── Cinematic hero ────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="
  position: relative;
  width: 100%;
  height: 440px;
  border-radius: 22px;
  overflow: hidden;
  margin-bottom: 2rem;
  border: 1px solid rgba(212,137,63,0.25);
  box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 50px rgba(212,137,63,0.05);
">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Taj_Mahal%2C_Agra%2C_India_edit3.jpg/1280px-Taj_Mahal%2C_Agra%2C_India_edit3.jpg"
    style="width:100%; height:100%; object-fit:cover; display:block;"
  />
  <div style="
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, rgba(15,11,30,0.95) 0%, rgba(15,11,30,0.6) 50%, rgba(15,11,30,0.15) 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3.5rem;
  ">
    <div style="
      display: inline-block;
      background: linear-gradient(135deg, rgba(212,137,63,0.15), rgba(201,168,76,0.1));
      border: 1px solid rgba(212,137,63,0.4);
      color: #D4893F;
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      padding: 0.35rem 1rem;
      border-radius: 999px;
      font-family: Philosopher, sans-serif;
      margin-bottom: 1.4rem;
      width: fit-content;
    ">{T("hero_badge")}</div>
    <div style="
      font-family: Cinzel, serif;
      font-size: 3rem;
      color: #F5E6D3;
      font-weight: 600;
      line-height: 1.15;
      margin-bottom: 1rem;
    ">{T("hero_title_1")}<br><span style="
      background: linear-gradient(135deg, #D4893F, #E8C97A);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    ">{T("hero_title_2")}</span></div>
    <p style="
      font-size: 1rem;
      color: #C4A882;
      max-width: 500px;
      line-height: 1.8;
      font-family: DM Sans, sans-serif;
      margin: 0;
    ">{T("hero_desc")}</p>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Core values of Indian heritage ────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; margin: 1rem 0 1.5rem 0;">
  <span class="value-pill">🙏 अहिंसा · Non-Violence</span>
  <span class="value-pill">🕉️ धर्म · Dharma</span>
  <span class="value-pill">📖 ज्ञान · Knowledge</span>
  <span class="value-pill">🤝 सेवा · Service</span>
  <span class="value-pill">🌿 प्रकृति · Nature</span>
</div>
""", unsafe_allow_html=True)

    # ── Ornamental divider ────────────────────────────────────────────────────
    st.markdown('<div class="ornament-divider">❖ ─── ✦ ─── ❖</div>', unsafe_allow_html=True)

    # Metrics
    st.markdown("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(f"🏛️ {T('monuments_covered')}", "8+", "Ancient to Modern")
    with m2:
        st.metric(f"🔮 {T('ai_powered')}", "Vision AI", "Gemini Powered")
    with m3:
        st.metric(f"🌍 {T('sdg_aligned')}", "SDG 11 & 17", "Sustainable Future")
    with m4:
        st.metric(f"⚡ {T('response_time')}", "< 2 sec", "Real-time AI")

    st.markdown("")

    # Feature cards — with cultural icons
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            f'<div class="heritage-card">'
            f'<div style="font-size:2.2rem;margin-bottom:0.8rem;">🪔</div>'
            f'<strong style="font-family:Cinzel,serif;color:#E8A85C;font-size:1.05rem;">{T("smart_recognition")}</strong>'
            f'<br><br><span style="color:#C4A882;">{T("smart_recognition_d")}</span></div>',
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            f'<div class="heritage-card">'
            f'<div style="font-size:2.2rem;margin-bottom:0.8rem;">📜</div>'
            f'<strong style="font-family:Cinzel,serif;color:#E8A85C;font-size:1.05rem;">{T("heritage_chatbot")}</strong>'
            f'<br><br><span style="color:#C4A882;">{T("heritage_chatbot_d")}</span></div>',
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            f'<div class="heritage-card">'
            f'<div style="font-size:2.2rem;margin-bottom:0.8rem;">🌿</div>'
            f'<strong style="font-family:Cinzel,serif;color:#E8A85C;font-size:1.05rem;">{T("sustainability_guide")}</strong>'
            f'<br><br><span style="color:#C4A882;">{T("sustainability_guide_d")}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        f'<div class="heritage-card">'
        f'<div style="font-size:2.2rem;margin-bottom:0.8rem;">🧠</div>'
        f'<strong style="font-family:Cinzel,serif;color:#E8A85C;font-size:1.05rem;">{T("knowledge_quiz")}</strong>'
        f'<br><br><span style="color:#C4A882;">{T("knowledge_quiz_d")}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── Ornamental divider ────────────────────────────────────────────────────
    st.markdown('<div class="ornament-divider">✦ ─── ❖ ─── ✦</div>', unsafe_allow_html=True)

    # ── Cultural Heritage Section ─────────────────────────────────────────────
    st.markdown("""
<div style="
  background: linear-gradient(135deg, rgba(122,46,59,0.08), rgba(212,137,63,0.06), rgba(27,16,64,0.15));
  border: 1px solid rgba(212,137,63,0.15);
  border-radius: 18px;
  padding: 2rem 2.5rem;
  margin: 1rem 0 2rem 0;
">
  <div style="font-family:'Cinzel',serif; font-size:1.3rem; color:#E8A85C; font-weight:500; margin-bottom:1rem;">
    🕉️ Our Heritage, Our Pride
  </div>
  <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1.5rem;">
    <div style="text-align:center;">
      <div style="font-size:2rem; margin-bottom:0.5rem;">🏛️</div>
      <div style="font-family:'Philosopher',sans-serif; font-weight:700; color:#E8C97A; font-size:0.9rem;">5000+ Years</div>
      <div style="color:#8A7560; font-size:0.8rem; margin-top:0.3rem;">Of continuous civilization</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:2rem; margin-bottom:0.5rem;">📖</div>
      <div style="font-family:'Philosopher',sans-serif; font-weight:700; color:#E8C97A; font-size:0.9rem;">40 UNESCO Sites</div>
      <div style="color:#8A7560; font-size:0.8rem; margin-top:0.3rem;">World Heritage landmarks</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:2rem; margin-bottom:0.5rem;">🙏</div>
      <div style="font-family:'Philosopher',sans-serif; font-weight:700; color:#E8C97A; font-size:0.9rem;">Unity in Diversity</div>
      <div style="color:#8A7560; font-size:0.8rem; margin-top:0.3rem;">Countless traditions & languages</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    with st.expander(T("how_to_use")):
        st.markdown("""
**Step 1:** Go to Monument Recognition and upload a monument photo

**Step 2:** View detailed history, architecture, and facts

**Step 3:** Chat with AI Heritage Chatbot about the monument

**Step 4:** Get Sustainability tips and take the Knowledge Quiz
""")

    st.markdown('<div class="ornament-divider">❖ ─── ✦ ─── ❖</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f"**{T('tech_stack')}**")
        st.caption("Python + Streamlit")
        st.caption("Google Gemini Vision AI")
        st.caption("Pillow + JSON")
    with a2:
        st.markdown(f"**{T('problem_solved')}**")
        st.caption("Lack of accessible heritage education")
        st.caption("Promoting responsible tourism")
        st.caption("AI-powered cultural preservation")
    with a3:
        st.markdown(f"**{T('impact')}**")
        st.caption("500M+ annual heritage visitors")
        st.caption("SDG 11 & 17 aligned")
        st.caption("Preserving 5000 years of culture")

    # ── Closing Sanskrit quote ────────────────────────────────────────────────
    st.markdown("""
<div class="culture-banner" style="margin-top:2rem;">
  <div style="font-family:'Cinzel',serif; font-size:1.2rem; color:#E8C97A; font-weight:500; margin-bottom:0.5rem;">
    "तमसो मा ज्योतिर्गमय"
  </div>
  <div style="font-family:'Philosopher',sans-serif; font-size:0.82rem; color:#C4A882; font-style:italic;">
    "Lead me from darkness to light" — Brihadaranyaka Upanishad
  </div>
</div>
""", unsafe_allow_html=True)

<<<<<<< HEAD
    # ── Hidden Gems Demo ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💎 Explore Hidden Gems")
    col_lat, col_lon = st.columns(2)
    with col_lat:
        user_lat = st.number_input("Your Latitude", value=27.1752, format="%0.5f")
    with col_lon:
        user_lon = st.number_input("Your Longitude", value=78.0420, format="%0.5f")
        
    user_id = "demo_user"
    if st.button("Check for Hidden Gems"):
        unlocked = check_nearby_gems(user_lat, user_lon, user_id)
        show_gem_unlock_ui(unlocked)

=======
>>>>>>> 07dc145c19582e5525ab4c2d7040077e47ce921b
# -----------------------------------------------------------------------------
# Monument Recognition page
# -----------------------------------------------------------------------------
elif active_page == "recognition":
    st.markdown(f"## {T('monument_recognition')}")

    # ── Manual monument selector (no button needed — on_change fires immediately) ──
    all_monuments = get_all_monument_names()
    all_options   = [T("select_placeholder")] + all_monuments

    def _on_manual_change():
        chosen = st.session_state.get("manual_select_key", T("select_placeholder"))
        if chosen == T("select_placeholder"):
            return
        details = get_monument_details(chosen)
        st.session_state["monument_result"] = {
            "monument_name": chosen,
            "location":      details.get("location", "India") if details else "India",
            "confidence":    "Manual Selection",
            "brief_description": details.get("cultural_importance", f"Explore {chosen}") if details else f"Explore {chosen}",
        }
        st.session_state["monument_details"]  = details
        st.session_state["uploaded_image"]    = None
        st.session_state["_last_uploaded_name"] = None
        if chosen not in st.session_state["monuments_visited"]:
            st.session_state["monuments_visited"].add(chosen)
            pts = award_xp("view_monument")
            st.toast(f"⚡ +{pts} XP for exploring {chosen}!", icon="✨")

    # Resolve current index so selectbox shows active monument
    current_result = st.session_state.get("monument_result")
    current_name   = current_result.get("monument_name") if current_result else None
    if current_name and current_result.get("confidence") == "Manual Selection" and current_name in all_options:
        sel_idx = all_options.index(current_name)
    else:
        sel_idx = 0

    st.selectbox(
        T("select_monument"),
        options=all_options,
        index=sel_idx,
        key="manual_select_key",
        on_change=_on_manual_change,
        help="Choose any monument to instantly load full historical details.",
    )

    st.markdown("---")

    # ── Image upload ──────────────────────────────────────────────────────────
    file_uploader_here = st.file_uploader(
        T("upload_label"),
        type=["jpg", "jpeg", "png"],
        key="recognition_uploader",
    )
    if file_uploader_here is not None:
        # Only re-run recognition when a NEW file is uploaded
        if st.session_state.get("_last_uploaded_name") != file_uploader_here.name:
            st.session_state["_last_uploaded_name"] = file_uploader_here.name
            st.session_state["uploaded_image"]      = file_uploader_here
            image_bytes = file_uploader_here.read()
            file_uploader_here.seek(0)

            with st.spinner(T("identifying")):
                result = get_demo_result(image_bytes, filename=file_uploader_here.name)
                st.session_state["monument_result"]  = result
                st.session_state["monument_details"] = get_monument_details(result.get("monument_name", ""))

            if result.get("monument_name") not in ("Unknown", None, ""):
                detected_name = result["monument_name"]
                st.toast(f"✅ Identified: {detected_name}", icon="🏛️")
                if detected_name not in st.session_state["monuments_visited"]:
                    st.session_state["monuments_visited"].add(detected_name)
                    pts = award_xp("view_monument")
                    st.toast(f"⚡ +{pts} XP for exploring {detected_name}!", icon="✨")
            else:
                st.warning("⚠️ Could not identify. Please rename your file to include the monument name (e.g. red_fort.jpg) or use the dropdown.")

    # ── Show result (from image upload OR manual selection) ───────────────────
    result       = st.session_state.get("monument_result")
    image_to_show = st.session_state.get("uploaded_image")

    # Monument cover images — local files from assets/sample_images/
    BASE_DIR = Path(__file__).parent
    MONUMENT_IMAGES = {
        "Taj Mahal":         BASE_DIR / "assets/sample_images/taj.jpg",
        "Red Fort":          BASE_DIR / "assets/sample_images/redfort.jpg",
        "Qutub Minar":       BASE_DIR / "assets/sample_images/qutubminar.jpg",
        "Hampi":             BASE_DIR / "assets/sample_images/hampi.jpg",
        "Konark Sun Temple": BASE_DIR / "assets/sample_images/konark.jpg",
        "Ajanta Caves":      BASE_DIR / "assets/sample_images/ajanta.jpg",
        "Hawa Mahal":        BASE_DIR / "assets/sample_images/hawamahal.jpg",
        "India Gate":        BASE_DIR / "assets/sample_images/indiagate.jpg",
    }

    if result is not None and result.get("monument_name") not in ("Unknown", None, ""):
        monument_name = result["monument_name"]

        # Identification result card
        col_img, col_result = st.columns(2)
        with col_img:
            if image_to_show is not None:
                image_to_show.seek(0)
                st.image(image_to_show, caption=f"Uploaded: {monument_name}", use_container_width=True)
            elif monument_name in MONUMENT_IMAGES and MONUMENT_IMAGES[monument_name].exists():
                st.image(
                    str(MONUMENT_IMAGES[monument_name]),
                    caption=monument_name,
                    use_container_width=True,
                )
            else:
                st.markdown(
                    f'<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;'
                    f'padding:3rem;text-align:center;font-size:2.5rem;">🏛️<br>'
                    f'<span style="font-size:1rem;color:var(--text-secondary);">{monument_name}</span></div>',
                    unsafe_allow_html=True,
                )
        with col_result:
            if result.get("confidence") == "Manual Selection":
                st.info(f"{T('manually_selected')}: **{monument_name}**")
            else:
                st.success(T("monument_identified"))
            st.markdown(f"**🏛️ Monument:** {result.get('monument_name', '—')}")
            st.markdown(f"**📍 Location:** {result.get('location', '—')}")
            st.markdown(f"**📊 Confidence:** {result.get('confidence', '—')}")
            st.markdown(f"**📝** {result.get('brief_description', '—')}")

        # render voice guide immediately beneath the monument title/card
        render_voice_guide(monument_name)
        # ── Detailed Information ──────────────────────────────────────────────
        monument_details = st.session_state.get("monument_details") or get_monument_details(monument_name)
        st.session_state["monument_details"] = monument_details

        if monument_details:
            st.markdown("---")
            st.markdown(f"### {T('detailed_info')}")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [T("tab_history"), T("tab_architecture"), T("tab_facts"), T("tab_fun"), T("tab_visitor")]
            )

            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**🧱 Built By:**\n\n{monument_details.get('built_by', '—')}")
                    st.markdown(f"**📅 Year Built:**\n\n{monument_details.get('year_built', '—')}")
                with col_b:
                    st.markdown(f"**📍 Location:**\n\n{monument_details.get('location', '—')}")
                    st.markdown(f"**🏗️ Type:**\n\n{monument_details.get('type', '—')}")
                st.markdown("---")
                st.markdown("**🌏 Cultural Importance:**")
                st.info(monument_details.get("cultural_importance", "—"))
                badge_col1, badge_col2 = st.columns(2)
                with badge_col1:
                    if monument_details.get("unesco"):
                        st.success("🏆 UNESCO World Heritage Site")
                with badge_col2:
                    if monument_details.get("seven_wonders"):
                        st.success("✨ One of the Seven Wonders of the World")

            with tab2:
                st.markdown("**🏛️ Architectural Style & Construction:**")
                st.info(monument_details.get("architecture", "—"))

            with tab3:
                key_facts = monument_details.get("key_facts", [])
                for i, fact in enumerate(key_facts, 1):
                    st.markdown(
                        f"""<div style="background:var(--bg-card);border:1px solid var(--border);
                        border-radius:8px;padding:0.8rem 1rem;margin:0.4rem 0;">
                        <span style="color:var(--gold);font-weight:700;">#{i}</span>
                        &nbsp;{fact}</div>""",
                        unsafe_allow_html=True,
                    )

            with tab4:
                fun_fact = monument_details.get("fun_fact", "")
                if fun_fact:
                    st.markdown(
                        f"""<div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.4);
                        border-radius:12px;padding:1.5rem;font-size:1.05rem;color:var(--gold-light);">
                        💡 {fun_fact}</div>""",
                        unsafe_allow_html=True,
                    )
                # Quick quiz teaser
                st.markdown("")
                st.markdown("**🧠 Want to test your knowledge?**")
                if st.button(T("go_to_quiz"), key="goto_quiz_btn"):
                    st.session_state["page_id"] = "quiz"
                    st.rerun()

            with tab5:
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    st.markdown(f"**🗓️ Best Time to Visit:**\n\n{monument_details.get('best_time_to_visit', '—')}")
                with col_v2:
                    st.markdown(f"**🎟️ Entry Fee:**\n\n{monument_details.get('entry_fee', '—')}")
                st.markdown("")
                st.info("🌿 Follow sustainable tourism guidelines → Visit the **Sustainability** tab for tips!")

            # ── Social Caption ────────────────────────────────────────────────
            st.markdown("---")
            st.markdown(f"### {T('share_exploration')}")
            caption = generate_caption(monument_name)
            st.text_area(
                T("copy_share"),
                value=caption,
                height=120,
                key="social_caption_area",
            )

        else:
            st.info(f"📚 Full details for **{monument_name}** are being added. Try selecting from the dropdown!")

    else:
        st.info(T("upload_or_select"))

# -----------------------------------------------------------------------------
# AI Chatbot page
# -----------------------------------------------------------------------------
elif active_page == "chatbot":
    st.markdown(f"## {T('ai_chatbot')}")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
        st.info(f"{T('chatting_about')}: **Taj Mahal**")
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")
        st.success(f"{T('chatting_about')}: {monument_name}")

    # Display chat history
    for message in st.session_state["chat_history"]:
        role = message.get("role", "")
        content = message.get("content", "")
        if role == "user":
            with st.chat_message("user"):
                st.write(content)
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.write(content)

    # Chat input
    user_input = st.chat_input(f"{T('ask_anything')} {monument_name}...")

    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        with st.spinner(T("thinking")):
            try:
                response = get_demo_response(user_input, monument_name)
            except Exception as e:
                response = f"I'd be happy to tell you about {monument_name}. Please ask me anything about its history, architecture, or culture!"

        st.session_state["chat_history"].append({"role": "assistant", "content": response})

        # XP: asking chatbot a question
        pts = award_xp("ask_chatbot")
        st.toast(f"⚡ +{pts} XP for your curiosity!", icon="💬")

        st.rerun()

    if st.button(T("clear_chat")):
        st.session_state["chat_history"] = []
        st.rerun()

# -----------------------------------------------------------------------------
# Sustainability page
# -----------------------------------------------------------------------------
elif active_page == "sustainability":
    st.markdown(f"## {T('sustainable_tourism')}")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")

    st.success(f"{T('sustainability_tips_for')}: {monument_name}")

    monument_details = st.session_state.get("monument_details")
    if "sustainability_tips" not in st.session_state or st.session_state.get("last_monument") != monument_name:
        with st.spinner("🌱 Loading sustainability tips..."):
            tips = get_demo_sustainability_tips(monument_name)
            st.session_state["sustainability_tips"] = tips
            st.session_state["last_monument"] = monument_name
            st.toast("Sustainability tips ready!", icon="🌿")

    tips = st.session_state.get("sustainability_tips", get_demo_sustainability_tips(monument_name))

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown(f"### {T('environmental_tips')}")
        for tip in tips.get("environmental_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown(f"### {T('cultural_respect')}")
        for tip in tips.get("cultural_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    with s3:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown(f"### {T('responsible_photo')}")
        for tip in tips.get("photography_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    conservation_message = tips.get("conservation_message", "")
    if conservation_message:
        st.info(f"💚 {conservation_message}")

# -----------------------------------------------------------------------------
# Quiz page
# -----------------------------------------------------------------------------
elif active_page == "quiz":
    st.markdown(f"## {T('heritage_quiz')}")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")

    if st.session_state.get("quiz_questions") is None or st.session_state.get("last_quiz_monument") != monument_name:
        quiz_questions = get_quiz_questions(monument_name)
        if quiz_questions:
            st.session_state["quiz_questions"] = quiz_questions
            st.session_state["last_quiz_monument"] = monument_name
            st.session_state["quiz_started"] = False
            st.session_state["quiz_completed"] = False
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
        else:
            st.info(f"📚 Quiz questions for {monument_name} are being added. Try with a Taj Mahal image!")
            st.stop()

    quiz_questions = st.session_state.get("quiz_questions", [])
    current_index = st.session_state.get("current_question_index", 0)
    quiz_started = st.session_state.get("quiz_started", False)
    quiz_completed = st.session_state.get("quiz_completed", False)
    quiz_answers = st.session_state.get("quiz_answers", [])

    st.success(f"{T('quiz_about')}: {monument_name}")

    if not quiz_started and not quiz_completed:
        st.markdown(f"**Test your knowledge about {monument_name}!**")
        st.markdown(f"This quiz has {len(quiz_questions)} questions.")
        if st.button(T("start_quiz"), type="primary"):
            st.session_state["quiz_started"] = True
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
            st.rerun()

    elif quiz_started and not quiz_completed:
        if current_index < len(quiz_questions):
            question_data = quiz_questions[current_index]
            question = question_data.get("question", "")
            options = question_data.get("options", [])
            answer = question_data.get("answer", "")

            st.markdown("---")
            st.markdown(f"### Question {current_index + 1} of {len(quiz_questions)}")
            st.markdown(f"**{question}**")

            selected_option = st.radio(
                "Select your answer:",
                options=options,
                key=f"quiz_option_{current_index}",
                label_visibility="collapsed",
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(T("submit_answer"), type="primary"):
                    is_correct = selected_option == answer
                    quiz_answers.append({
                        "question": question,
                        "selected": selected_option,
                        "correct": answer,
                        "is_correct": is_correct,
                        "explanation": question_data.get("explanation", ""),
                    })
                    st.session_state["quiz_answers"] = quiz_answers
                    if current_index + 1 < len(quiz_questions):
                        st.session_state["current_question_index"] = current_index + 1
                    else:
                        st.session_state["quiz_completed"] = True
                        st.session_state["quizzes_completed"] += 1
                        correct_count = sum(1 for ans in quiz_answers if ans.get("is_correct", False))
                        # XP: completing a quiz
                        pts = award_xp("complete_quiz")
                        st.toast(f"🧠 Quiz complete! Score: {correct_count}/{len(quiz_questions)} | +{pts} XP", icon="🧠")
                    st.rerun()
            with col2:
                if current_index > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state["current_question_index"] = current_index - 1
                        st.rerun()

    elif quiz_completed:
        st.markdown("---")
        st.markdown(f"### {T('quiz_completed')}")

        correct_count = sum(1 for ans in quiz_answers if ans.get("is_correct", False))
        total_questions = len(quiz_answers)
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0

        st.markdown(f"**Your Score: {correct_count}/{total_questions} ({score_percentage:.0f}%)**")

        if score_percentage == 100:
            st.success("🌟 Perfect score! You're a heritage expert!")
            st.snow()
        elif score_percentage >= 80:
            st.success("🎯 Excellent! Great knowledge of Indian heritage!")
        elif score_percentage >= 60:
            st.info("👍 Good job! Keep learning about India's monuments!")
        else:
            st.warning("📚 Keep studying! Visit the monument details to learn more!")

        st.markdown("---")
        st.markdown(f"### {T('review_answers')}")
        for idx, ans in enumerate(quiz_answers):
            with st.expander(f"Question {idx + 1}: {ans.get('question', '')}"):
                if ans.get("is_correct", False):
                    st.success(f"✅ Correct! You selected: {ans.get('selected', '')}")
                else:
                    st.error(f"❌ Incorrect. You selected: {ans.get('selected', '')}")
                    st.info(f"✅ Correct answer: {ans.get('correct', '')}")
                st.markdown(f"**Explanation:** {ans.get('explanation', '')}")

        if st.button(T("retake_quiz")):
            st.session_state["quiz_started"] = False
            st.session_state["quiz_completed"] = False
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
            st.rerun()

        # ── Social caption after quiz ────────────────────────────────────────
        st.markdown("---")
        st.markdown(f"### {T('share_achievement')}")
        quiz_caption = (
            f"🧠 Just scored {correct_count}/{total_questions} on the {monument_name} quiz on Sanskriti AI!\n"
            f"Testing my heritage knowledge and loving it.\n"
            f"#SanskritiAI #QuizMaster #IncredibleIndia #{monument_name.replace(' ', '')}"
        )
        st.text_area(T("copy_share"), value=quiz_caption, height=110, key="quiz_caption_area")

# -----------------------------------------------------------------------------
# Achievements page
# -----------------------------------------------------------------------------
elif active_page == "achievements":
    render_dashboard("demo_user")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="
  margin-top: 4rem;
  padding: 1.5rem 0;
  border-top: 1px solid rgba(212,137,63,0.15);
  text-align: center;
">
  <div style="color:rgba(201,168,76,0.25); font-size:1rem; letter-spacing:0.5em; margin-bottom:0.8rem;">
    ❖ ─── ✦ ─── ❖
  </div>
  <div style="font-family:'Cinzel',serif; font-size:0.8rem; color:#8A7560; letter-spacing:0.1em; margin-bottom:0.3rem;">
    {T("footer_left")}
  </div>
  <div style="font-family:'Philosopher',sans-serif; font-size:0.72rem; color:#6A5C48; letter-spacing:0.08em;">
    {T("footer_right")}
  </div>
</div>
""", unsafe_allow_html=True)
