# Live Matches Page - Cricket Analytics Dashboard
# Real-time match data from Cricbuzz API

import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import time

def show_live_matches(api_key):
    """Display live cricket matches data from Cricbuzz API"""
    
    st.markdown("# 📺 Live Cricket Matches")
    st.markdown("Real-time cricket match data from Cricbuzz API")
    
    if not api_key:
        st.warning("⚠️ Please enter your RapidAPI key in the sidebar to view live matches")
        st.markdown("""
        ### How to get your API key:
        1. Visit [RapidAPI Cricbuzz Cricket API](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)
        2. Subscribe to the free plan (0 cost)
        3. Copy your X-RapidAPI-Key
        4. Paste it in the sidebar
        """)
        return
    
    # API configuration
    base_url = "https://cricbuzz-cricket.p.rapidapi.com"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    # Auto-refresh option
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    with col3:
        st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    try:
        # Fetch live matches
        with st.spinner("Fetching live matches..."):
            matches_response = requests.get(f"{base_url}/matches/v1/live", headers=headers, timeout=10)
            
            if matches_response.status_code == 200:
                matches_data = matches_response.json()
                display_live_matches(matches_data, headers, base_url)
            elif matches_response.status_code == 401:
                st.error("❌ Invalid API key. Please check your RapidAPI key.")
            elif matches_response.status_code == 429:
                st.error("❌ API rate limit exceeded. Please wait and try again.")
            else:
                st.error(f"❌ API Error: {matches_response.status_code}")
                
    except requests.exceptions.Timeout:
        st.error("❌ Request timeout. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {str(e)}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

def display_live_matches(matches_data, headers, base_url):
    """Display formatted live matches data"""
    
    if not matches_data or 'typeMatches' not in matches_data:
        st.info("📭 No live matches currently available")
        return
    
    # Display live matches by category
    for match_type in matches_data.get('typeMatches', []):
        match_type_name = match_type.get('matchType', 'Unknown')
        series_matches = match_type.get('seriesMatches', [])
        
        if not series_matches:
            continue
            
        st.markdown(f"## 🏏 {match_type_name}")
        
        for series in series_matches:
            series_name = series.get('seriesAdWrapper', {}).get('seriesName', 'Unknown Series')
            matches = series.get('seriesAdWrapper', {}).get('matches', [])
            
            if matches:
                st.markdown(f"### 🏆 {series_name}")
                
                for match in matches:
                    match_info = match.get('matchInfo', {})
                    match_score = match.get('matchScore', {})
                    
                    display_match_card(match_info, match_score, headers, base_url)

def display_match_card(match_info, match_score, headers, base_url):
    """Display individual match card with detailed information"""
    
    match_id = match_info.get('matchId')
    match_desc = match_info.get('matchDesc', 'Match')
    venue = match_info.get('venueInfo', {})
    
    # Create match card
    with st.container():
        st.markdown(f"""
        <div style="border: 2px solid #1f77b4; border-radius: 10px; padding: 1rem; margin: 1rem 0; background-color: #f8f9fa;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**📋 {match_desc}**")
            if venue:
                venue_name = venue.get('ground', 'Unknown Venue')
                city = venue.get('city', 'Unknown City')
                st.markdown(f"🏟️ {venue_name}, {city}")
            
            # Match status
            state = match_info.get('state', 'Unknown')
            status = match_info.get('status', 'Unknown Status')
            st.markdown(f"⏱️ **Status:** {state} - {status}")
        
        with col2:
            # Team scores
            if match_score and 'team1Score' in match_score:
                team1_score = match_score.get('team1Score', {})
                team2_score = match_score.get('team2Score', {})
                
                team1_name = team1_score.get('teamName', 'Team 1')
                team1_runs = team1_score.get('inngs1', {}).get('runs', 0)
                team1_wickets = team1_score.get('inngs1', {}).get('wickets', 0)
                team1_overs = team1_score.get('inngs1', {}).get('overs', 0)
                
                team2_name = team2_score.get('teamName', 'Team 2')
                team2_runs = team2_score.get('inngs1', {}).get('runs', 0)
                team2_wickets = team2_score.get('inngs1', {}).get('wickets', 0)
                team2_overs = team2_score.get('inngs1', {}).get('overs', 0)
                
                st.markdown(f"**{team1_name}:** {team1_runs}/{team1_wickets} ({team1_overs})")
                st.markdown(f"**{team2_name}:** {team2_runs}/{team2_wickets} ({team2_overs})")
            else:
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                st.markdown(f"**Teams:** {team1} vs {team2}")
        
        with col3:
            # Detailed view button
            if st.button(f"📊 View Details", key=f"match_{match_id}"):
                show_match_details(match_id, headers, base_url)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_match_details(match_id, headers, base_url):
    """Show detailed match information including scorecard and commentary"""
    
    if not match_id:
        st.error("Match ID not available")
        return
    
    st.markdown(f"## 📊 Match Details - ID: {match_id}")
    
    # Tabs for different match information
    tab1, tab2, tab3 = st.tabs(["📊 Scorecard", "💬 Commentary", "📋 Match Info"])
    
    with tab1:
        show_scorecard(match_id, headers, base_url)
    
    with tab2:
        show_commentary(match_id, headers, base_url)
    
    with tab3:
        show_match_info(match_id, headers, base_url)

def show_scorecard(match_id, headers, base_url):
    """Display match scorecard"""
    
    try:
        with st.spinner("Loading scorecard..."):
            scorecard_response = requests.get(
                f"{base_url}/mcenter/v1/{match_id}/scard",
                headers=headers,
                timeout=10
            )
            
            if scorecard_response.status_code == 200:
                scorecard_data = scorecard_response.json()
                
                # Display scorecard information
                if 'scoreCard' in scorecard_data:
                    for innings in scorecard_data['scoreCard']:
                        innings_info = innings.get('inningsInfo', {})
                        bat_team = innings_info.get('batTeamDetails', {})
                        
                        st.markdown(f"### 🏏 {bat_team.get('batTeamName', 'Team')} Innings")
                        
                        # Batting scorecard
                        if 'batTeamDetails' in innings_info:
                            batting_data = []
                            for batsman in bat_team.get('batsmenData', {}).values():
                                if isinstance(batsman, dict) and 'batName' in batsman:
                                    batting_data.append({
                                        'Player': batsman.get('batName', ''),
                                        'Runs': batsman.get('runs', 0),
                                        'Balls': batsman.get('balls', 0),
                                        'Fours': batsman.get('fours', 0),
                                        'Sixes': batsman.get('sixes', 0),
                                        'Strike Rate': batsman.get('strikeRate', 0)
                                    })
                            
                            if batting_data:
                                df_batting = pd.DataFrame(batting_data)
                                st.dataframe(df_batting, use_container_width=True)
                        
                        # Bowling scorecard
                        bowl_team = innings_info.get('bowlTeamDetails', {})
                        if bowl_team:
                            bowling_data = []
                            for bowler in bowl_team.get('bowlersData', {}).values():
                                if isinstance(bowler, dict) and 'bowlName' in bowler:
                                    bowling_data.append({
                                        'Bowler': bowler.get('bowlName', ''),
                                        'Overs': bowler.get('overs', 0),
                                        'Runs': bowler.get('runs', 0),
                                        'Wickets': bowler.get('wickets', 0),
                                        'Economy': bowler.get('economy', 0)
                                    })
                            
                            if bowling_data:
                                st.markdown("**Bowling Figures:**")
                                df_bowling = pd.DataFrame(bowling_data)
                                st.dataframe(df_bowling, use_container_width=True)
                
                else:
                    st.info("📭 Scorecard data not available for this match")
                    
            else:
                st.error(f"Failed to load scorecard: {scorecard_response.status_code}")
                
    except Exception as e:
        st.error(f"Error loading scorecard: {str(e)}")

def show_commentary(match_id, headers, base_url):
    """Display match commentary"""
    
    try:
        with st.spinner("Loading commentary..."):
            commentary_response = requests.get(
                f"{base_url}/mcenter/v1/{match_id}/comm",
                headers=headers,
                timeout=10
            )
            
            if commentary_response.status_code == 200:
                commentary_data = commentary_response.json()
                
                if 'commentaryList' in commentary_data:
                    st.markdown("### 💬 Live Commentary")
                    
                    for comment in commentary_data['commentaryList'][:10]:  # Show latest 10 comments
                        if 'commText' in comment:
                            over_number = comment.get('overNumber', '')
                            ball_number = comment.get('ballNumber', '')
                            comm_text = comment.get('commText', '')
                            
                            if over_number and ball_number:
                                st.markdown(f"**{over_number}.{ball_number}** - {comm_text}")
                            else:
                                st.markdown(f"• {comm_text}")
                            st.markdown("---")
                else:
                    st.info("📭 Commentary not available for this match")
                    
            else:
                st.error(f"Failed to load commentary: {commentary_response.status_code}")
                
    except Exception as e:
        st.error(f"Error loading commentary: {str(e)}")

def show_match_info(match_id, headers, base_url):
    """Display detailed match information"""
    
    try:
        with st.spinner("Loading match information..."):
            info_response = requests.get(
                f"{base_url}/mcenter/v1/{match_id}",
                headers=headers,
                timeout=10
            )
            
            if info_response.status_code == 200:
                info_data = info_response.json()
                
                if 'matchHeader' in info_data:
                    match_header = info_data['matchHeader']
                    
                    # Match details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📋 Match Information")
                        st.markdown(f"**Match Type:** {match_header.get('matchType', 'N/A')}")
                        st.markdown(f"**Series:** {match_header.get('seriesName', 'N/A')}")
                        st.markdown(f"**Match Number:** {match_header.get('matchDescription', 'N/A')}")
                        
                        # Team information
                        team1 = match_header.get('team1', {})
                        team2 = match_header.get('team2', {})
                        st.markdown(f"**Team 1:** {team1.get('name', 'N/A')}")
                        st.markdown(f"**Team 2:** {team2.get('name', 'N/A')}")
                    
                    with col2:
                        st.markdown("### 🏟️ Venue Information")
                        venue_info = match_header.get('venueInfo', {})
                        st.markdown(f"**Ground:** {venue_info.get('ground', 'N/A')}")
                        st.markdown(f"**City:** {venue_info.get('city', 'N/A')}")
                        st.markdown(f"**Country:** {venue_info.get('country', 'N/A')}")
                        
                        # Match timing
                        st.markdown("### ⏰ Match Timing")
                        match_start = match_header.get('matchStartTimestamp')
                        if match_start:
                            start_time = datetime.fromtimestamp(match_start / 1000)
                            st.markdown(f"**Start Time:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        
                        result = match_header.get('result', 'Match in progress')
                        st.markdown(f"**Result:** {result}")
                
                else:
                    st.info("📭 Match information not available")
                    
            else:
                st.error(f"Failed to load match information: {info_response.status_code}")
                
    except Exception as e:
        st.error(f"Error loading match information: {str(e)}")

def display_sample_data():
    """Display sample match data when API is not available"""
    
    st.info("📝 Displaying sample data (API key required for live data)")
    
    # Sample match data
    sample_matches = [
        {
            'match': 'IND vs AUS - 3rd ODI',
            'venue': 'Wankhede Stadium, Mumbai',
            'status': 'Live',
            'team1': 'India',
            'team1_score': '287/6 (45.2 ov)',
            'team2': 'Australia',
            'team2_score': '245 (48.1 ov)',
            'result': 'India won by 42 runs'
        },
        {
            'match': 'ENG vs NZ - 2nd Test',
            'venue': 'Lord\'s, London',
            'status': 'Day 3',
            'team1': 'England',
            'team1_score': '435 & 89/2 (25 ov)',
            'team2': 'New Zealand',
            'team2_score': '378',
            'result': 'England lead by 146 runs'
        }
    ]
    
    for i, match in enumerate(sample_matches):
        with st.container():
            st.markdown(f"""
            <div style="border: 2px solid #1f77b4; border-radius: 10px; padding: 1rem; margin: 1rem 0; background-color: #f8f9fa;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**📋 {match['match']}**")
                st.markdown(f"🏟️ {match['venue']}")
                st.markdown(f"⏱️ **Status:** {match['status']}")
            
            with col2:
                st.markdown(f"**{match['team1']}:** {match['team1_score']}")
                st.markdown(f"**{match['team2']}:** {match['team2_score']}")
                if match['result']:
                    st.markdown(f"**Result:** {match['result']}")
            
            with col3:
                st.button(f"📊 View Details", key=f"sample_match_{i}", disabled=True)
            
            st.markdown("</div>", unsafe_allow_html=True)