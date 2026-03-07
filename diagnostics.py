import os
import sqlite3
from pathlib import Path
import sys

# Add project root to path for imports to work correctly
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from modules.gamification.hidden_gems import check_nearby_gems


def print_success(msg):
    print(f"✓ {msg}")

def print_error(msg):
    print(f"✗ {msg}")


def verify_project_structure():
    print("\n--- 1. Verifying Project Structure ---")
    
    folders_to_check = [
        "modules/gamification",
        "data",
        "assets",
        ".streamlit"
    ]
    
    files_to_check = [
        "modules/gamification/database_setup.py",
        "modules/gamification/seed_hidden_gems.py",
        "modules/gamification/hidden_gems.py",
        "modules/gamification/test_unlock.py",
        "modules/gamification/view_gems.py" # Assuming we made this previously
    ]
    
    all_passed = True
    
    for folder in folders_to_check:
        folder_path = project_root / folder
        if folder_path.exists() and folder_path.is_dir():
            pass
        else:
            print_error(f"Missing directory: {folder}")
            all_passed = False
            
    for f in files_to_check:
        file_path = project_root / f
        if file_path.exists() and file_path.is_file():
            pass
        else:
            print_error(f"Missing file: {f}")
            all_passed = False
            
    if all_passed:
        print_success("Project structure valid")
    return all_passed


def verify_database():
    print("\n--- 2. Verifying Database ---")
    db_path = project_root / "data" / "gamification.db"
    
    if not db_path.exists():
        print_error(f"Database not found at {db_path}")
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ["hidden_gems", "unlocked_gems", "user_progress"]
        all_passed = True
        for table in required_tables:
            if table not in tables:
                print_error(f"Missing table: {table}")
                all_passed = False
        
        if all_passed:
            print_success("Database connected")
            
            # Print schemas
            for table in required_tables:
                cursor.execute(f"PRAGMA table_info({table})")
                schema = cursor.fetchall()
                print(f"  Schema for {table}:")
                for column in schema:
                    print(f"    - {column[1]} ({column[2]})")
                    
        return all_passed
        
    except Exception as e:
        print_error(f"Database verification failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def verify_hidden_gem_data():
    print("\n--- 3. Verifying Hidden Gem Data ---")
    db_path = project_root / "data" / "gamification.db"
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM hidden_gems")
        gems = cursor.fetchall()
        
        if not gems:
            print_error("Hidden gems table is empty.")
            return False
            
        print_success("Hidden gems seeded")
        print(f"  Found {len(gems)} gems:")
        for gem in gems:
            print(f"    - {gem['monument_name']}: {gem['gem_name']} ({gem['latitude']}, {gem['longitude']}) - XP: {gem['xp_reward']}")
            
        return True
        
    except Exception as e:
        print_error(f"Hidden gem data verification failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def verify_unlock_system_and_xp():
    print("\n--- 4 & 5. Verifying Unlock System & XP Tracking ---")
    db_path = project_root / "data" / "gamification.db"
    
    # Coordinates for testing (Taj Mahal area)
    test_lat = 27.1752
    test_lon = 78.0420
    user_id = "demo_user"
    
    try:
        # Clear existing test data to ensure clean check
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM unlocked_gems WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM user_progress WHERE user_id = ?", (user_id,))
        cursor.execute("INSERT INTO user_progress (user_id, xp, level, monuments_visited) VALUES (?, 0, 1, 0)", (user_id,))
        conn.commit()
        
        # Initial XP check
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        start_xp = cursor.fetchone()[0]
        
        # Run unlock function
        unlocked = check_nearby_gems(test_lat, test_lon, user_id)
        
        if not unlocked:
            print_error("No gems unlocked when they should have been.")
            return False, False, False
            
        print_success("GPS unlock working")
        print(f"  Unlocked {len(unlocked)} gems.")
        
        # Check XP after unlock
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        new_xp = cursor.fetchone()[0]
        
        expected_xp = start_xp + sum(gem['xp_reward'] for gem in unlocked)
        
        if new_xp == expected_xp and new_xp > start_xp:
            print_success("XP tracking working")
            print(f"  Current XP for '{user_id}': {new_xp} (Started at {start_xp})")
            return True, True, True
        else:
            print_error(f"XP tracking failed. Expected {expected_xp}, got {new_xp}")
            return True, False, False
            
    except Exception as e:
        print_error(f"Unlock system verification failed: {e}")
        return False, False, False
    finally:
        if 'conn' in locals():
            conn.close()


def verify_duplicate_protection():
    print("\n--- 6. Verifying Duplicate Protection ---")
    
    # The setup from step 4 leaves the gem unlocked. 
    # Calling it again should return empty list and not increase XP.
    test_lat = 27.1752
    test_lon = 78.0420
    user_id = "demo_user"
    db_path = project_root / "data" / "gamification.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        start_xp = cursor.fetchone()[0]
        
        unlocked_again = check_nearby_gems(test_lat, test_lon, user_id)
        
        cursor.execute("SELECT xp FROM user_progress WHERE user_id = ?", (user_id,))
        new_xp = cursor.fetchone()[0]
        
        if not unlocked_again and new_xp == start_xp:
            print_success("Duplicate protection working")
            return True
        else:
            print_error(f"Duplicate protection failed. Returned: {unlocked_again}, XP changed: {start_xp} -> {new_xp}")
            return False
            
    except Exception as e:
        print_error(f"Duplicate protection verification failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def verify_streamlit_integration():
    print("\n--- 7. Verifying Streamlit Integration ---")
    app_path = project_root / "app.py"
    
    if not app_path.exists():
        print_error("app.py not found.")
        return False
        
    try:
        with open(app_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        import_found = "modules.gamification.hidden_gems" in content
        lat_input_found = "Your Latitude" in content or "user_lat" in content and "number_input" in content
        lon_input_found = "Your Longitude" in content or "user_lon" in content and "number_input" in content
        button_found = "Check for Hidden Gems" in content and "button" in content
        
        if import_found and lat_input_found and lon_input_found and button_found:
            print_success("Streamlit integration detected")
            return True
        else:
            missing = []
            if not import_found: missing.append("Import statment")
            if not lat_input_found: missing.append("Latitude input")
            if not lon_input_found: missing.append("Longitude input")
            if not button_found: missing.append("Button check")
            
            print_error(f"Streamlit integration incomplete. Missing: {', '.join(missing)}")
            return False
            
    except Exception as e:
        print_error(f"Streamlit integration verification failed: {e}")
        return False


if __name__ == "__main__":
    print("====================================")
    print("SANSKRITI-AI GAMIFICATION DIAGNOSTIC")
    print("====================================")
    
    s1 = verify_project_structure()
    s2 = verify_database()
    s3 = verify_hidden_gem_data()
    s4, s5, _ = verify_unlock_system_and_xp()
    s6 = verify_duplicate_protection()
    s7 = verify_streamlit_integration()
    
    print("\n====================================")
    print("FINAL REPORT SUMMARY")
    print("====================================")
    print(f"{'✓' if s1 else '✗'} Project structure valid")
    print(f"{'✓' if s2 else '✗'} Database connected")
    print(f"{'✓' if s3 else '✗'} Hidden gems seeded")
    print(f"{'✓' if s4 else '✗'} GPS unlock working")
    print(f"{'✓' if s5 else '✗'} XP tracking working")
    print(f"{'✓' if s6 else '✗'} Duplicate protection working")
    print(f"{'✓' if s7 else '✗'} Streamlit integration detected")
    print("====================================\n")
