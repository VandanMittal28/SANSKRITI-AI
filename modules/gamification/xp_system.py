import sqlite3
from pathlib import Path

def get_db_path():
    current_dir = Path(__file__).resolve().parent
    return current_dir.parent.parent / "data" / "gamification.db"

LEVELS = [
    (0, "Beginner Explorer"),
    (50, "Explorer"),
    (150, "Heritage Seeker"),
    (300, "Cultural Guardian"),
    (600, "Sanskriti Master")
]

def get_level_info(xp):
    current_level_idx = 0
    for i, (req_xp, title) in enumerate(LEVELS):
        if xp >= req_xp:
            current_level_idx = i
        else:
            break
            
    current_title = LEVELS[current_level_idx][1]
    
    next_level_info = None
    if current_level_idx + 1 < len(LEVELS):
        next_req_xp, next_title = LEVELS[current_level_idx + 1]
        next_level_info = {
            "title": next_title,
            "req_xp": next_req_xp,
            "xp_needed": next_req_xp - xp
        }
        
    return current_level_idx + 1, current_title, next_level_info

def award_xp(user_id, xp_amount):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        cursor = conn.cursor()
        
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            cursor.execute("INSERT INTO user_progress (user_id, xp, level, monuments_visited) VALUES (?, ?, 1, 0)", (user_id, xp_amount))
            old_xp = 0
        else:
            old_xp = row[0]
            cursor.execute("UPDATE user_progress SET xp = xp + ? WHERE user_id = ?", (xp_amount, user_id))
            
        new_xp = old_xp + xp_amount
        old_level, old_title, _ = get_level_info(old_xp)
        new_level, new_title, _ = get_level_info(new_xp)
        
        leveled_up = new_level > old_level
        
        if leveled_up:
            cursor.execute("UPDATE user_progress SET level = ? WHERE user_id = ?", (new_level, user_id))
            
        conn.commit()
        
        return {
            "old_xp": old_xp,
            "new_xp": new_xp,
            "old_level": old_level,
            "new_level": new_level,
            "old_title": old_title,
            "new_title": new_title,
            "leveled_up": leveled_up
        }
    except Exception as e:
        print(f"Error awarding XP: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def get_full_user_stats(user_id):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_progress WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            return {
                "user_id": user_id,
                "xp": 0,
                "level": 1,
                "title": LEVELS[0][1],
                "monuments_visited": 0,
                "next_level_info": get_level_info(0)[2]
            }
            
        xp = row["xp"]
        _, title, next_level_info = get_level_info(xp)
        
        return {
            "user_id": user_id,
            "xp": xp,
            "level": row["level"],
            "title": title,
            "monuments_visited": row["monuments_visited"],
            "next_level_info": next_level_info
        }
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
