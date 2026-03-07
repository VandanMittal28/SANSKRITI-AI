import sqlite3
import os
from pathlib import Path

def view_hidden_gems():
    """
    Connect to the gamification database and print all rows from the hidden_gems table.
    """
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    db_path = project_root / "data" / "gamification.db"
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return
        
    try:
        conn = sqlite3.connect(db_path)
        # return rows as dictionaries for nicer printing
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM hidden_gems")
        rows = cursor.fetchall()
        
        if not rows:
            print("The hidden_gems table is currently empty.")
            return
            
        print(f"--- Found {len(rows)} Hidden Gems ---\n")
        
        for row in rows:
            print(f"ID: {row['id']}")
            print(f"Monument: {row['monument_name']}")
            print(f"Gem Name: {row['gem_name']}")
            print(f"Location: {row['latitude']}, {row['longitude']}")
            print(f"Unlock Radius: {row['unlock_radius']}m")
            print(f"Story: {row['story']}")
            print(f"XP Reward: {row['xp_reward']}")
            print("-" * 40)
            
    except sqlite3.Error as e:
        print(f"An error occurred reading from the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    view_hidden_gems()
