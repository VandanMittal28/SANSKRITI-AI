import sqlite3
import streamlit as st
import os
from pathlib import Path
from geopy.distance import geodesic
from modules.gamification.xp_system import award_xp
from modules.gamification.achievements import check_and_award_badges

def get_db_path():
    """Helper connection to gamification.db"""
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    return project_root / "data" / "gamification.db"

def get_user_unlocked_gems(user_id):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT h.*, u.unlocked_at 
            FROM hidden_gems h 
            JOIN unlocked_gems u ON h.id = u.gem_id 
            WHERE u.user_id = ?
        ''', (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching unlocked gems: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def check_nearby_gems(user_lat, user_lon, user_id):
    """
    Checks if a user is near any hidden gems. If they are, unlocks the gem,
    awards XP, and returns a list of the newly unlocked gems.
    
    Args:
        user_lat (float): The user's current latitude
        user_lon (float): The user's current longitude
        user_id (str): The unique identifier for the user
        
    Returns:
        list: A list of dicts containing the newly unlocked gem details
    """
    db_path = get_db_path()
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return []
        
    newly_unlocked_gems = []
    user_location = (user_lat, user_lon)
    
    try:
        # We need a context manager because we're modifying records based on logic
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 1. Ensure user exists in user_progress before evaluating
        cursor.execute("SELECT user_id FROM user_progress WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO user_progress (user_id, xp, level, monuments_visited) VALUES (?, 0, 1, 0)", (user_id,))
            conn.commit()
            
        # 2. Fetch all hidden gems 
        cursor.execute("SELECT * FROM hidden_gems")
        all_gems = cursor.fetchall()
        
        for gem in all_gems:
            gem_id = gem["id"]
            gem_lat = gem["latitude"]
            gem_lon = gem["longitude"]
            gem_location = (gem_lat, gem_lon)
            unlock_radius_meters = gem["unlock_radius"]
            
            # 3. Use geopy.distance to calculate distance (in meters)
            distance_meters = geodesic(user_location, gem_location).meters
            
            # --- DEBUGGING OUTPUT ---
            print(f"Distance to {gem['gem_name']}: {distance_meters:.2f} meters")
            import os
            if os.environ.get("STREAMLIT_RUNTIME"):
                st.write(f"Distance to {gem['gem_name']}: {distance_meters:.2f} meters")
            # ------------------------
            
            # 4. If distance is within radius...
            if distance_meters <= unlock_radius_meters:
                
                # Check if gem is already unlocked for this user
                cursor.execute(
                    "SELECT * FROM unlocked_gems WHERE user_id = ? AND gem_id = ?", 
                    (user_id, gem_id)
                )
                
                if cursor.fetchone():
                    print(f"Gem already unlocked for this user: {gem['gem_name']}")
                    if os.environ.get("STREAMLIT_RUNTIME"):
                        st.write(f"Gem already unlocked for this user: {gem['gem_name']}")
                else:
                    print("Gem not unlocked yet, eligible for unlock.")
                    if os.environ.get("STREAMLIT_RUNTIME"):
                        st.write("Gem not unlocked yet, eligible for unlock.")
                        
                    # Mark as newly unlocked
                    
                    # Insert into unlocked_gems
                    cursor.execute(
                        "INSERT INTO unlocked_gems (user_id, gem_id) VALUES (?, ?)", 
                        (user_id, gem_id)
                    )
                    # Convert sqlite3.Row to dict and append to output list
                    gem_dict = dict(gem)
                    gem_dict["distance"] = round(distance_meters, 2) # Adding exactly how close they were
                    
                    # Successfully commit the new updates 
                    conn.commit()
                    
                    # Award XP atomically
                    xp_reward = gem["xp_reward"]
                    xp_result = award_xp(user_id, xp_reward)
                    gem_dict["xp_result"] = xp_result
                    
                    # Check and award badges atomically
                    cursor.execute("SELECT monuments_visited FROM user_progress WHERE user_id = ?", (user_id,))
                    row = cursor.fetchone()
                    monuments_visited = row[0] if row else 0
                    
                    new_badges = check_and_award_badges(user_id, xp_result["new_xp"] if xp_result else xp_reward, monuments_visited)
                    gem_dict["new_badges"] = new_badges
                    
                    newly_unlocked_gems.append(gem_dict)
                    
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Database error during gem check: {e}")
        if 'conn' in locals():
            conn.rollback()
    except Exception as e:
        print(f"Error calculating distance or updating gems: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            
    # 5. Returns unlocked gems (or empty list if none)
    return newly_unlocked_gems

def show_gem_unlock_ui(unlocked_gems):
    """
    Displays a structured and styled Streamlit success message for each unlocked gem.
    If no gems are available, shows a warning message encouraging exploration.
    """
    if not unlocked_gems:
        st.warning("No hidden gems nearby yet. Explore the monument area!")
        return

    for gem in unlocked_gems:
        st.success("🎉 Hidden Gem Discovered!")
        st.subheader(gem['gem_name'])
        st.write("XP Earned:", gem['xp_reward'])
        st.info(gem['story'])
        
        xp_res = gem.get("xp_result")
        if xp_res and xp_res.get("leveled_up"):
            st.success(f"🎊 Level Up! You are now a {xp_res.get('new_title')} (Level {xp_res.get('new_level')})")
            
        new_badges = gem.get("new_badges")
        if new_badges:
            for badge in new_badges:
                st.info(f"{badge['icon']} Badge Unlocked: {badge['title']} - {badge['desc']}")
