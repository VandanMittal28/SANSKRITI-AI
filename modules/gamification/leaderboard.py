import sqlite3
from pathlib import Path

def get_db_path():
    current_dir = Path(__file__).resolve().parent
    return current_dir.parent.parent / "data" / "gamification.db"

def get_leaderboard(limit=10):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, xp, level, monuments_visited
            FROM user_progress
            ORDER BY xp DESC, monuments_visited DESC
            LIMIT ?
        ''', (limit,))
        
        leaderboard = []
        for idx, row in enumerate(cursor.fetchall()):
            user_data = dict(row)
            user_data['rank'] = idx + 1
            leaderboard.append(user_data)
        
        return leaderboard
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_user_rank(user_id):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        user_xp = row[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_progress WHERE xp > ?", (user_xp,))
        higher_xp_count = cursor.fetchone()[0]
        
        return higher_xp_count + 1
        
    except Exception as e:
        print(f"Error fetching user rank: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()
