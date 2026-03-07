import sqlite3
import os
from pathlib import Path

def seed_hidden_gems():
    """
    Seed the gamification database with initial hidden gems data.
    Only seeds if the hidden_gems table is currently empty.
    """
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    db_path = project_root / "data" / "gamification.db"
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}. Please run database_setup.py first.")
        return
        
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table is empty
    try:
        cursor.execute("SELECT COUNT(*) FROM hidden_gems")
        count = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        print("Error: Table 'hidden_gems' does not exist. Please run database_setup.py first.")
        conn.close()
        return
    
    # Only insert if the table is empty
    if count == 0:
        hidden_gems_data = [
            (
                "Taj Mahal", 
                "Whispering Gallery", 
                27.1751, 
                78.0421, 
                30, 
                "The Taj Mahal dome creates a whispering acoustic effect where sounds travel across the chamber.", 
                50
            ),
            (
                "Red Fort", 
                "Secret Escape Tunnel", 
                28.6562, 
                77.2410, 
                30, 
                "The Red Fort once had secret tunnels used by the royal family for escape during emergencies.", 
                50
            ),
            (
                "Qutub Minar", 
                "Iron Pillar Mystery", 
                28.5245, 
                77.1855, 
                30, 
                "The iron pillar near Qutub Minar has resisted rust for over 1600 years.", 
                40
            )
        ]
        
        cursor.executemany('''
            INSERT INTO hidden_gems (monument_name, gem_name, latitude, longitude, unlock_radius, story, xp_reward)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', hidden_gems_data)
        
        conn.commit()
        print(f"Successfully seeded {len(hidden_gems_data)} hidden gems into the database.")
    else:
        print(f"Database already contains {count} hidden gems. Seeding skipped.")
        
    conn.close()

if __name__ == "__main__":
    seed_hidden_gems()
