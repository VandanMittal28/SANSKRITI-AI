import sqlite3
from pathlib import Path

def get_db_path():
    current_dir = Path(__file__).resolve().parent
    return current_dir.parent.parent / "data" / "gamification.db"

BADGES = {
    "first_discovery": {"id": "first_discovery", "title": "First Discovery", "icon": "💎", "desc": "Unlocked your first hidden gem", "condition": "gems >= 1"},
    "gem_hunter": {"id": "gem_hunter", "title": "Gem Hunter", "icon": "🗺️", "desc": "Unlocked 3 hidden gems", "condition": "gems >= 3"},
    "explorer": {"id": "explorer", "title": "Explorer", "icon": "🧭", "desc": "Earned 50 XP", "condition": "xp >= 50"},
    "heritage_seeker": {"id": "heritage_seeker", "title": "Heritage Seeker", "icon": "🏛️", "desc": "Earned 150 XP", "condition": "xp >= 150"},
    "cultural_guardian": {"id": "cultural_guardian", "title": "Cultural Guardian", "icon": "🔱", "desc": "Earned 300 XP", "condition": "xp >= 300"},
    "sanskriti_master": {"id": "sanskriti_master", "title": "Sanskriti Master", "icon": "👑", "desc": "Earned 600 XP", "condition": "xp >= 600"},
    "monument_explorer": {"id": "monument_explorer", "title": "Monument Explorer", "icon": "📸", "desc": "Visited 5 monuments", "condition": "monuments >= 5"},
    "quiz_master": {"id": "quiz_master", "title": "Quiz Master", "icon": "🧠", "desc": "Got a perfect score on a quiz", "condition": "quiz_perfect"}
}

def check_and_award_badges(user_id, xp, monuments_visited, quiz_perfect=False):
    db_path = get_db_path()
    new_badges = []
    
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        cursor = conn.cursor()
        
        # Get already earned badges
        cursor.execute("SELECT badge_id FROM user_badges WHERE user_id = ?", (user_id,))
        earned_badges = {row[0] for row in cursor.fetchall()}
        
        # Determine gem count
        from modules.gamification.hidden_gems import get_user_unlocked_gems
        unlocked_gems = get_user_unlocked_gems(user_id)
        gems_count = len(unlocked_gems)
        
        # Check conditions
        to_award = []
        if "first_discovery" not in earned_badges and gems_count >= 1:
            to_award.append("first_discovery")
        if "gem_hunter" not in earned_badges and gems_count >= 3:
            to_award.append("gem_hunter")
        if "explorer" not in earned_badges and xp >= 50:
            to_award.append("explorer")
        if "heritage_seeker" not in earned_badges and xp >= 150:
            to_award.append("heritage_seeker")
        if "cultural_guardian" not in earned_badges and xp >= 300:
            to_award.append("cultural_guardian")
        if "sanskriti_master" not in earned_badges and xp >= 600:
            to_award.append("sanskriti_master")
        if "monument_explorer" not in earned_badges and monuments_visited >= 5:
            to_award.append("monument_explorer")
        if "quiz_master" not in earned_badges and quiz_perfect:
            to_award.append("quiz_master")
            
        for badge_id in to_award:
            cursor.execute('''
                INSERT OR IGNORE INTO user_badges (user_id, badge_id)
                VALUES (?, ?)
            ''', (user_id, badge_id))
            if cursor.rowcount > 0:
                new_badges.append(BADGES[badge_id])
                
        conn.commit()
    except Exception as e:
        print(f"Error checking and awarding badges: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            
    return new_badges

def get_user_badges(user_id):
    db_path = get_db_path()
    badges = []
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("SELECT badge_id, earned_at FROM user_badges WHERE user_id = ?", (user_id,))
        for row in cursor.fetchall():
            badge_info = BADGES.get(row[0], None)
            if badge_info:
                badge_info = badge_info.copy()
                badge_info['earned_at'] = row[1]
                badges.append(badge_info)
    except Exception as e:
        print(f"Error fetching user badges: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return badges
