import sqlite3
import os
from pathlib import Path

def init_db():
    """
    Initialize the gamification database and create necessary tables.
    The database will be created at data/gamification.db relative to the project root.
    """
    # Determine the project root directory based on this script's location
    # This script is in modules/gamification, so root is 2 levels up
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    
    db_dir = project_root / "data"
    db_path = db_dir / "gamification.db"
    
    # Ensure the data directory exists
    db_dir.mkdir(parents=True, exist_ok=True)
    
    # Connect to the SQLite database
    # It will automatically create the database file if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the hidden_gems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hidden_gems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monument_name TEXT,
        gem_name TEXT,
        latitude REAL,
        longitude REAL,
        unlock_radius INTEGER,
        story TEXT,
        xp_reward INTEGER
    )
    ''')
    
    # Create the user_progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        monuments_visited INTEGER DEFAULT 0
    )
    ''')
    
    # Create the unlocked_gems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS unlocked_gems (
        user_id TEXT,
        gem_id INTEGER,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_badges (
        user_id TEXT,
        badge_id TEXT,
        earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, badge_id)
    )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"Gamification database initialized successfully at: {db_path}")

if __name__ == "__main__":
    init_db()
