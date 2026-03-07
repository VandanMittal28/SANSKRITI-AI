import streamlit as st
import pandas as pd
from modules.gamification.xp_system import get_full_user_stats, get_level_info, LEVELS
from modules.gamification.achievements import get_user_badges, BADGES
from modules.gamification.hidden_gems import get_user_unlocked_gems
from modules.gamification.leaderboard import get_leaderboard, get_user_rank
from modules.gamification.certification import generate_certificate, CERTIFICATE_MILESTONES

def render_dashboard(user_id):
    st.markdown("## 🎮 Gamification Dashboard")
    
    # Get user stats
    stats = get_full_user_stats(user_id)
    if not stats:
        st.warning("User statistics not found. Complete an activity to start earning XP!")
        return
        
    xp = stats["xp"]
    level = stats["level"]
    title = stats["title"]
    monuments = stats["monuments_visited"]
    next_level = stats["next_level_info"]
    
    # 1. Level Banner
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #1A0E30 0%, #291a40 100%);
                padding: 2rem; border-radius: 12px; border: 2px solid #C9A84C;
                text-align: center; margin-bottom: 2rem;">
        <h3 style="color: #D4893F; font-family: 'Cinzel', serif; margin: 0;">Level {level}</h3>
        <h1 style="color: #C9A84C; font-family: 'Cinzel', serif; margin: 0.5rem 0; font-size: 2.5rem;">{title}</h1>
        <p style="color: #F5E6D3; margin: 0; font-size: 1.2rem;">Total XP: {xp}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 2. XP Progress Bar
    if next_level:
        req_xp = next_level["req_xp"]
        # Convert to relative progress for this level tier
        # Need previous level xp requirement
        prev_req_xp = 0
        for i, (rxp, t) in enumerate(LEVELS):
            if rxp == req_xp:
                if i > 0:
                    prev_req_xp = LEVELS[i-1][0]
                break
                
        level_range = req_xp - prev_req_xp
        current_progress = xp - prev_req_xp
        progress_pct = max(0.0, min(1.0, current_progress / level_range))
        
        st.progress(progress_pct)
        st.caption(f"{xp} XP / {req_xp} XP for {next_level['title']}")
    else:
        st.progress(1.0)
        st.caption("Max Level Reached!")
        
    # 3. Stat Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("XP", xp)
    with c2:
        st.metric("Level", level)
    with c3:
        st.metric("Monuments Visited", monuments)
    with c4:
        rank = get_user_rank(user_id)
        st.metric("Global Rank", f"#{rank}" if rank else "Unranked")
        
    st.markdown("---")
    
    # 4. Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏅 Badges", "💎 Hidden Gems", "🏆 Leaderboard", "📜 Certificates"])
    
    with tab1:
        user_badges = get_user_badges(user_id)
        earned_badge_ids = [b["id"] for b in user_badges]
        
        st.markdown("### Your Badges")
        
        # Display all badges, dimming the locked ones
        cols = st.columns(4)
        for i, (badge_id, badge_info) in enumerate(BADGES.items()):
            col = cols[i % 4]
            is_earned = badge_id in earned_badge_ids
            opacity = 1.0 if is_earned else 0.3
            border = "1px solid #C9A84C" if is_earned else "1px solid #444"
            
            with col:
                st.markdown(f'''
                <div style="opacity: {opacity}; text-align: center; padding: 1rem; border: {border}; border-radius: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{badge_info['icon']}</div>
                    <div style="font-weight: bold; color: {'#C9A84C' if is_earned else 'gray'};">{badge_info['title']}</div>
                    <div style="font-size: 0.8rem; color: gray;">{badge_info['desc']}</div>
                </div>
                ''', unsafe_allow_html=True)

    with tab2:
        gems = get_user_unlocked_gems(user_id)
        if not gems:
            st.info("You haven't unlocked any hidden gems yet. Continue exploring monuments!")
        else:
            for gem in gems:
                st.markdown(f'''
                <div style="padding: 1rem; border: 1px solid #C9A84C; border-left: 5px solid #D4893F; border-radius: 5px; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: #D4893F;">{gem['gem_name']} @ {gem['monument_name']}</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #ccc;">{gem['story']}</p>
                    <small style="color: #8A7560;">Unlocked: {gem['unlocked_at'].split()[0]} | XP Earned: {gem['xp_reward']}</small>
                </div>
                ''', unsafe_allow_html=True)

    with tab3:
        leaders = get_leaderboard(limit=10)
        if not leaders:
            st.info("No leaderboard data available.")
        else:
            st.markdown("### Top Explorers")
            df = pd.DataFrame(leaders)
            df = df[['rank', 'user_id', 'xp', 'level', 'monuments_visited']]
            df.columns = ['Rank', 'Explorer', 'XP', 'Level', 'Monuments']
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### Verify Your Knowledge")
        st.write("Reach specific XP milestones to unlock official PDF certificates.")
        
        for cert_title, req_xp in CERTIFICATE_MILESTONES.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{cert_title} Certificate** (Requires {req_xp} XP)")
            with col2:
                if xp >= req_xp:
                    if st.button("Generate PDF", key=f"cert_{cert_title}"):
                        cert_path = generate_certificate(user_id, cert_title)
                        if cert_path:
                            with open(cert_path, "rb") as pdf_file:
                                st.download_button(
                                    label="Download PDF",
                                    data=pdf_file,
                                    file_name=f"{user_id}_{cert_title.replace(' ', '_')}.pdf",
                                    mime="application/pdf",
                                    key=f"dl_{cert_title}"
                                )
                else:
                    st.button("Locked", disabled=True, key=f"lock_{cert_title}")
