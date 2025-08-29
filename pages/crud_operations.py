# CRUD Operations Page - Cricket Analytics Dashboard
# Create, Read, Update, Delete operations for player and match data

import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.db_connection import DatabaseConnection

def show_crud_operations():
    """Display CRUD operations interface"""
    
    st.markdown("# ⚙️ CRUD Operations - Data Management")
    st.markdown("Create, Read, Update, and Delete operations for cricket database")
    
    # Initialize database connection
    try:
        db = DatabaseConnection()
        
        # Main tabs for different CRUD operations
        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Create Records", 
            "📖 Read Records", 
            "✏️ Update Records", 
            "🗑️ Delete Records"
        ])
        
        with tab1:
            show_create_operations(db)
        
        with tab2:
            show_read_operations(db)
        
        with tab3:
            show_update_operations(db)
        
        with tab4:
            show_delete_operations(db)
            
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        st.info("Please ensure the database is properly initialized.")

def show_create_operations(db):
    """Create new records interface"""
    
    st.markdown("## ➕ Create New Records")
    st.markdown("Add new players, matches, teams, venues, and series to the database")
    
    # Sub-tabs for different record types
    create_tabs = st.tabs(["👥 Add Player", "🏏 Add Match", "🏟️ Add Venue", "🏆 Add Team", "📅 Add Series"])
    
    with create_tabs[0]:
        create_player_form(db)
    
    with create_tabs[1]:
        create_match_form(db)
    
    with create_tabs[2]:
        create_venue_form(db)
    
    with create_tabs[3]:
        create_team_form(db)
    
    with create_tabs[4]:
        create_series_form(db)

def create_player_form(db):
    """Form to create new player"""
    
    st.markdown("### 👥 Add New Player")
    
    with st.form("add_player_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Player Name *", placeholder="e.g., Virat Kohli")
            country = st.selectbox("Country *", [
                "", "India", "Australia", "England", "New Zealand", "Pakistan", 
                "South Africa", "West Indies", "Bangladesh", "Sri Lanka", "Afghanistan", "Other"
            ])
            playing_role = st.selectbox("Playing Role *", [
                "", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"
            ])
            batting_style = st.selectbox("Batting Style", [
                "", "Right-hand bat", "Left-hand bat"
            ])
        
        with col2:
            bowling_style = st.selectbox("Bowling Style", [
                "", "Right-arm fast", "Left-arm fast", "Right-arm medium", 
                "Left-arm medium", "Right-arm off-break", "Left-arm orthodox", 
                "Right-arm leg-break", "Left-arm wrist-spin"
            ])
            date_of_birth = st.date_input("Date of Birth", value=None)
            total_runs = st.number_input("Total Runs", min_value=0, value=0)
            total_wickets = st.number_input("Total Wickets", min_value=0, value=0)
            batting_average = st.number_input("Batting Average", min_value=0.0, value=0.0, format="%.2f")
            bowling_average = st.number_input("Bowling Average", min_value=0.0, value=0.0, format="%.2f")
        
        col3, col4 = st.columns(2)
        with col3:
            strike_rate = st.number_input("Strike Rate", min_value=0.0, value=0.0, format="%.2f")
        with col4:
            economy_rate = st.number_input("Economy Rate", min_value=0.0, value=0.0, format="%.2f")
        
        submitted = st.form_submit_button("➕ Add Player", type="primary")
        
        if submitted:
            if not name or not country or not playing_role:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    query = """
                    INSERT INTO players (
                        name, country, playing_role, batting_style, bowling_style,
                        date_of_birth, total_runs, total_wickets, batting_average,
                        bowling_average, strike_rate, economy_rate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    params = (
                        name, country, playing_role, batting_style or None, bowling_style or None,
                        date_of_birth, total_runs, total_wickets, batting_average,
                        bowling_average, strike_rate, economy_rate
                    )
                    
                    db.execute_query(query, params, fetch=False)
                    st.success(f"✅ Player '{name}' added successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error adding player: {str(e)}")

def create_match_form(db):
    """Form to create new match"""
    
    st.markdown("### 🏏 Add New Match")
    
    with st.form("add_match_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            match_title = st.text_input("Match Title *", placeholder="e.g., IND vs AUS - 3rd ODI")
            team1 = st.text_input("Team 1 *", placeholder="e.g., India")
            team2 = st.text_input("Team 2 *", placeholder="e.g., Australia")
            venue_name = st.text_input("Venue Name", placeholder="e.g., Wankhede Stadium")
            venue_city = st.text_input("Venue City", placeholder="e.g., Mumbai")
            venue_country = st.text_input("Venue Country", placeholder="e.g., India")
        
        with col2:
            match_date = st.date_input("Match Date *", value=date.today())
            match_format = st.selectbox("Match Format *", ["", "Test", "ODI", "T20I", "T10"])
            toss_winner = st.text_input("Toss Winner", placeholder="e.g., India")
            toss_decision = st.selectbox("Toss Decision", ["", "Bat", "Bowl"])
            winner = st.text_input("Winner", placeholder="e.g., India")
            victory_margin = st.text_input("Victory Margin", placeholder="e.g., 5 wickets, 42 runs")
            victory_type = st.selectbox("Victory Type", ["", "Runs", "Wickets", "Tie", "No Result"])
            man_of_match = st.text_input("Man of the Match", placeholder="e.g., Virat Kohli")
            match_status = st.selectbox("Match Status", ["Scheduled", "Live", "Completed", "Cancelled"])
        
        submitted = st.form_submit_button("➕ Add Match", type="primary")
        
        if submitted:
            if not match_title or not team1 or not team2 or not match_format:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    query = """
                    INSERT INTO matches (
                        match_title, team1, team2, venue_name, venue_city, venue_country,
                        match_date, match_format, toss_winner, toss_decision, winner,
                        victory_margin, victory_type, man_of_match, match_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    params = (
                        match_title, team1, team2, venue_name or None, venue_city or None, venue_country or None,
                        match_date, match_format, toss_winner or None, toss_decision or None, winner or None,
                        victory_margin or None, victory_type or None, man_of_match or None, match_status
                    )
                    
                    db.execute_query(query, params, fetch=False)
                    st.success(f"✅ Match '{match_title}' added successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error adding match: {str(e)}")

def create_venue_form(db):
    """Form to create new venue"""
    
    st.markdown("### 🏟️ Add New Venue")
    
    with st.form("add_venue_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            venue_name = st.text_input("Venue Name *", placeholder="e.g., Lord's Cricket Ground")
            city = st.text_input("City *", placeholder="e.g., London")
            country = st.text_input("Country *", placeholder="e.g., England")
        
        with col2:
            capacity = st.number_input("Capacity", min_value=0, value=0)
            pitch_type = st.selectbox("Pitch Type", [
                "", "Batting-friendly", "Bowling-friendly", "Balanced", "Spin-friendly", "Fast-bowling friendly"
            ])
        
        submitted = st.form_submit_button("➕ Add Venue", type="primary")
        
        if submitted:
            if not venue_name or not city or not country:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    query = """
                    INSERT INTO venues (venue_name, city, country, capacity, pitch_type)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    
                    params = (venue_name, city, country, capacity or None, pitch_type or None)
                    
                    db.execute_query(query, params, fetch=False)
                    st.success(f"✅ Venue '{venue_name}' added successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error adding venue: {str(e)}")

def create_team_form(db):
    """Form to create new team"""
    
    st.markdown("### 🏆 Add New Team")
    
    with st.form("add_team_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            team_name = st.text_input("Team Name *", placeholder="e.g., India")
            country = st.text_input("Country *", placeholder="e.g., India")
            team_type = st.selectbox("Team Type", ["", "International", "Domestic", "Franchise"])
        
        with col2:
            matches_played = st.number_input("Matches Played", min_value=0, value=0)
            matches_won = st.number_input("Matches Won", min_value=0, value=0)
            matches_lost = st.number_input("Matches Lost", min_value=0, value=0)
            matches_tied = st.number_input("Matches Tied", min_value=0, value=0)
        
        submitted = st.form_submit_button("➕ Add Team", type="primary")
        
        if submitted:
            if not team_name or not country:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    # Calculate win percentage
                    win_percentage = (matches_won / matches_played * 100) if matches_played > 0 else 0
                    
                    query = """
                    INSERT INTO teams (
                        team_name, country, team_type, matches_played, matches_won,
                        matches_lost, matches_tied, win_percentage
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    params = (
                        team_name, country, team_type or None, matches_played,
                        matches_won, matches_lost, matches_tied, win_percentage
                    )
                    
                    db.execute_query(query, params, fetch=False)
                    st.success(f"✅ Team '{team_name}' added successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error adding team: {str(e)}")

def create_series_form(db):
    """Form to create new series"""
    
    st.markdown("### 📅 Add New Series")
    
    with st.form("add_series_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            series_name = st.text_input("Series Name *", placeholder="e.g., India vs Australia ODI Series 2025")
            series_type = st.selectbox("Series Type", ["", "Bilateral", "Tri-series", "Tournament", "World Cup"])
            host_country = st.text_input("Host Country *", placeholder="e.g., India")
        
        with col2:
            start_date = st.date_input("Start Date *", value=date.today())
            end_date = st.date_input("End Date", value=None)
            total_matches = st.number_input("Total Matches", min_value=1, value=3)
            matches_completed = st.number_input("Matches Completed", min_value=0, value=0)
        
        submitted = st.form_submit_button("➕ Add Series", type="primary")
        
        if submitted:
            if not series_name or not host_country:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    query = """
                    INSERT INTO series (
                        series_name, series_type, host_country, start_date,
                        end_date, total_matches, matches_completed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    params = (
                        series_name, series_type or None, host_country, start_date,
                        end_date, total_matches, matches_completed
                    )
                    
                    db.execute_query(query, params, fetch=False)
                    st.success(f"✅ Series '{series_name}' added successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error adding series: {str(e)}")

def show_read_operations(db):
    """Read/Browse records interface"""
    
    st.markdown("## 📖 Browse Records")
    st.markdown("View and search existing records in the database")
    
    # Table selection
    table_options = ["players", "matches", "teams", "venues", "series", "player_statistics"]
    selected_table = st.selectbox("Select Table to Browse:", table_options)
    
    # Search and filter options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search", placeholder="Enter search term...")
    
    with col2:
        limit = st.number_input("Records to show", min_value=10, max_value=1000, value=50)
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    try:
        # Build query based on table and search
        if search_term:
            if selected_table == "players":
                query = f"""
                SELECT * FROM {selected_table} 
                WHERE name LIKE ? OR country LIKE ? OR playing_role LIKE ?
                ORDER BY name
                LIMIT ?
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", limit)
            elif selected_table == "matches":
                query = f"""
                SELECT * FROM {selected_table}
                WHERE match_title LIKE ? OR team1 LIKE ? OR team2 LIKE ? OR venue_name LIKE ?
                ORDER BY match_date DESC
                LIMIT ?
                """
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", limit)
            else:
                query = f"SELECT * FROM {selected_table} LIMIT ?"
                params = (limit,)
        else:
            query = f"SELECT * FROM {selected_table} LIMIT ?"
            params = (limit,)
        
        # Execute query
        data = db.execute_query(query, params)
        
        if not data.empty:
            st.markdown(f"### 📋 {selected_table.title()} Records ({len(data)} found)")
            
            # Display data with pagination
            st.dataframe(data, use_container_width=True, height=400)
            
            # Download option
            csv_data = data.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {selected_table} CSV",
                data=csv_data,
                file_name=f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Quick stats
            st.markdown("### 📊 Quick Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(data))
            
            if selected_table == "players":
                with col2:
                    countries = data['country'].nunique()
                    st.metric("Countries", countries)
                with col3:
                    avg_runs = data['total_runs'].mean() if 'total_runs' in data.columns else 0
                    st.metric("Avg Runs", f"{avg_runs:.1f}")
            
            elif selected_table == "matches":
                with col2:
                    formats = data['match_format'].nunique() if 'match_format' in data.columns else 0
                    st.metric("Formats", formats)
                with col3:
                    completed = len(data[data['match_status'] == 'Completed']) if 'match_status' in data.columns else 0
                    st.metric("Completed", completed)
        
        else:
            st.info(f"📭 No records found in {selected_table} table.")
            
    except Exception as e:
        st.error(f"❌ Error reading data: {str(e)}")

def show_update_operations(db):
    """Update existing records interface"""
    
    st.markdown("## ✏️ Update Records")
    st.markdown("Modify existing records in the database")
    
    # Table selection for update
    table_options = ["players", "matches", "teams", "venues", "series"]
    selected_table = st.selectbox("Select Table to Update:", table_options, key="update_table")
    
    if selected_table == "players":
        update_player_records(db)
    elif selected_table == "matches":
        update_match_records(db)
    elif selected_table == "teams":
        update_team_records(db)
    elif selected_table == "venues":
        update_venue_records(db)
    elif selected_table == "series":
        update_series_records(db)

def update_player_records(db):
    """Update player records"""
    
    st.markdown("### ✏️ Update Player Records")
    
    # First, select player to update
    try:
        players_query = "SELECT player_id, name, country FROM players ORDER BY name"
        players_data = db.execute_query(players_query)
        
        if players_data.empty:
            st.info("No players found in database.")
            return
        
        # Player selection
        player_options = {f"{row['name']} ({row['country']})": row['player_id'] 
                         for _, row in players_data.iterrows()}
        
        selected_player_name = st.selectbox("Select Player to Update:", [""] + list(player_options.keys()))
        
        if selected_player_name:
            player_id = player_options[selected_player_name]
            
            # Get current player data
            current_data_query = "SELECT * FROM players WHERE player_id = ?"
            current_data = db.execute_query(current_data_query, (player_id,))
            
            if not current_data.empty:
                player_data = current_data.iloc[0]
                
                # Update form
                with st.form("update_player_form"):
                    st.markdown(f"**Updating:** {player_data['name']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        name = st.text_input("Player Name", value=player_data['name'])
                        country = st.text_input("Country", value=player_data['country'] or "")
                        playing_role = st.selectbox("Playing Role", 
                            ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
                            index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(player_data['playing_role']) 
                            if player_data['playing_role'] in ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"] else 0
                        )
                        total_runs = st.number_input("Total Runs", value=int(player_data['total_runs'] or 0))
                        total_wickets = st.number_input("Total Wickets", value=int(player_data['total_wickets'] or 0))
                    
                    with col2:
                        batting_average = st.number_input("Batting Average", value=float(player_data['batting_average'] or 0))
                        bowling_average = st.number_input("Bowling Average", value=float(player_data['bowling_average'] or 0))
                        strike_rate = st.number_input("Strike Rate", value=float(player_data['strike_rate'] or 0))
                        economy_rate = st.number_input("Economy Rate", value=float(player_data['economy_rate'] or 0))
                    
                    submitted = st.form_submit_button("💾 Update Player", type="primary")
                    
                    if submitted:
                        try:
                            update_query = """
                            UPDATE players SET 
                                name = ?, country = ?, playing_role = ?, total_runs = ?, total_wickets = ?,
                                batting_average = ?, bowling_average = ?, strike_rate = ?, economy_rate = ?,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE player_id = ?
                            """
                            
                            params = (
                                name, country, playing_role, total_runs, total_wickets,
                                batting_average, bowling_average, strike_rate, economy_rate, player_id
                            )
                            
                            db.execute_query(update_query, params, fetch=False)
                            st.success(f"✅ Player '{name}' updated successfully!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error updating player: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error loading players: {str(e)}")

def update_match_records(db):
    """Update match records"""
    
    st.markdown("### ✏️ Update Match Records")
    
    try:
        matches_query = "SELECT match_id, match_title, match_date FROM matches ORDER BY match_date DESC LIMIT 50"
        matches_data = db.execute_query(matches_query)
        
        if matches_data.empty:
            st.info("No matches found in database.")
            return
        
        # Match selection
        match_options = {f"{row['match_title']} ({row['match_date']})": row['match_id'] 
                        for _, row in matches_data.iterrows()}
        
        selected_match_name = st.selectbox("Select Match to Update:", [""] + list(match_options.keys()))
        
        if selected_match_name:
            match_id = match_options[selected_match_name]
            
            # Get current match data
            current_data_query = "SELECT * FROM matches WHERE match_id = ?"
            current_data = db.execute_query(current_data_query, (match_id,))
            
            if not current_data.empty:
                match_data = current_data.iloc[0]
                
                # Update form
                with st.form("update_match_form"):
                    st.markdown(f"**Updating:** {match_data['match_title']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        winner = st.text_input("Winner", value=match_data['winner'] or "")
                        victory_margin = st.text_input("Victory Margin", value=match_data['victory_margin'] or "")
                        victory_type = st.selectbox("Victory Type", 
                            ["", "Runs", "Wickets", "Tie", "No Result"],
                            index=0 if not match_data['victory_type'] else 
                            ["", "Runs", "Wickets", "Tie", "No Result"].index(match_data['victory_type'])
                        )
                    
                    with col2:
                        man_of_match = st.text_input("Man of the Match", value=match_data['man_of_match'] or "")
                        match_status = st.selectbox("Match Status", 
                            ["Scheduled", "Live", "Completed", "Cancelled"],
                            index=["Scheduled", "Live", "Completed", "Cancelled"].index(match_data['match_status']) 
                            if match_data['match_status'] in ["Scheduled", "Live", "Completed", "Cancelled"] else 0
                        )
                    
                    submitted = st.form_submit_button("💾 Update Match", type="primary")
                    
                    if submitted:
                        try:
                            update_query = """
                            UPDATE matches SET 
                                winner = ?, victory_margin = ?, victory_type = ?,
                                man_of_match = ?, match_status = ?
                            WHERE match_id = ?
                            """
                            
                            params = (winner or None, victory_margin or None, victory_type or None,
                                    man_of_match or None, match_status, match_id)
                            
                            db.execute_query(update_query, params, fetch=False)
                            st.success(f"✅ Match updated successfully!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error updating match: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error loading matches: {str(e)}")

def update_team_records(db):
    """Update team records"""
    
    st.markdown("### ✏️ Update Team Records")
    st.info("Select team and update statistics")
    
    # Similar implementation for teams...
    st.markdown("*Team update functionality - implementation similar to player updates*")

def update_venue_records(db):
    """Update venue records"""
    
    st.markdown("### ✏️ Update Venue Records")
    st.info("Select venue and update information")
    
    # Similar implementation for venues...
    st.markdown("*Venue update functionality - implementation similar to player updates*")

def update_series_records(db):
    """Update series records"""
    
    st.markdown("### ✏️ Update Series Records")
    st.info("Select series and update details")
    
    # Similar implementation for series...
    st.markdown("*Series update functionality - implementation similar to player updates*")

def show_delete_operations(db):
    """Delete records interface"""
    
    st.markdown("## 🗑️ Delete Records")
    st.warning("⚠️ **Caution:** Delete operations are permanent and cannot be undone!")
    
    # Safety confirmation
    confirm_delete = st.checkbox("I understand that delete operations are permanent")
    
    if not confirm_delete:
        st.info("Please confirm you understand the risks before proceeding with delete operations.")
        return
    
    # Table selection for delete
    table_options = ["players", "matches", "teams", "venues", "series"]
    selected_table = st.selectbox("Select Table for Delete Operation:", table_options, key="delete_table")
    
    if selected_table == "players":
        delete_player_records(db)
    elif selected_table == "matches":
        delete_match_records(db)
    else:
        st.info(f"Delete functionality for {selected_table} - Select specific records to delete")

def delete_player_records(db):
    """Delete player records"""
    
    st.markdown("### 🗑️ Delete Player Records")
    
    try:
        players_query = "SELECT player_id, name, country FROM players ORDER BY name"
        players_data = db.execute_query(players_query)
        
        if players_data.empty:
            st.info("No players found in database.")
            return
        
        # Player selection
        player_options = {f"{row['name']} ({row['country']})": row['player_id'] 
                         for _, row in players_data.iterrows()}
        
        selected_players = st.multiselect("Select Player(s) to Delete:", list(player_options.keys()))
        
        if selected_players:
            st.warning(f"⚠️ You are about to delete {len(selected_players)} player(s):")
            for player in selected_players:
                st.markdown(f"- {player}")
            
            # Final confirmation
            final_confirm = st.text_input(
                "Type 'DELETE' to confirm:", 
                placeholder="Type DELETE to proceed"
            )
            
            if final_confirm == "DELETE":
                if st.button("🗑️ Permanently Delete Selected Players", type="secondary"):
                    try:
                        deleted_count = 0
                        for player_name in selected_players:
                            player_id = player_options[player_name]
                            
                            # Delete player statistics first (foreign key constraint)
                            db.execute_query("DELETE FROM player_statistics WHERE player_id = ?", (player_id,), fetch=False)
                            
                            # Delete player
                            db.execute_query("DELETE FROM players WHERE player_id = ?", (player_id,), fetch=False)
                            deleted_count += 1
                        
                        st.success(f"✅ Successfully deleted {deleted_count} player(s)!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error deleting players: {str(e)}")
            else:
                if final_confirm:
                    st.error("Please type 'DELETE' exactly to confirm")
    
    except Exception as e:
        st.error(f"❌ Error loading players: {str(e)}")

def delete_match_records(db):
    """Delete match records"""
    
    st.markdown("### 🗑️ Delete Match Records")
    
    try:
        matches_query = "SELECT match_id, match_title, match_date FROM matches ORDER BY match_date DESC LIMIT 50"
        matches_data = db.execute_query(matches_query)
        
        if matches_data.empty:
            st.info("No matches found in database.")
            return
        
        # Match selection
        match_options = {f"{row['match_title']} ({row['match_date']})": row['match_id'] 
                        for _, row in matches_data.iterrows()}
        
        selected_matches = st.multiselect("Select Match(es) to Delete:", list(match_options.keys()))
        
        if selected_matches:
            st.warning(f"⚠️ You are about to delete {len(selected_matches)} match(es):")
            for match in selected_matches:
                st.markdown(f"- {match}")
            
            # Final confirmation
            final_confirm = st.text_input(
                "Type 'DELETE' to confirm:", 
                placeholder="Type DELETE to proceed",
                key="delete_matches_confirm"
            )
            
            if final_confirm == "DELETE":
                if st.button("🗑️ Permanently Delete Selected Matches", type="secondary"):
                    try:
                        deleted_count = 0
                        for match_name in selected_matches:
                            match_id = match_options[match_name]
                            
                            # Delete player statistics first
                            db.execute_query("DELETE FROM player_statistics WHERE match_id = ?", (match_id,), fetch=False)
                            
                            # Delete match
                            db.execute_query("DELETE FROM matches WHERE match_id = ?", (match_id,), fetch=False)
                            deleted_count += 1
                        
                        st.success(f"✅ Successfully deleted {deleted_count} match(es)!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error deleting matches: {str(e)}")
            else:
                if final_confirm:
                    st.error("Please type 'DELETE' exactly to confirm")
    
    except Exception as e:
        st.error(f"❌ Error loading matches: {str(e)}")

# Bulk operations section
def show_bulk_operations(db):
    """Bulk operations for data management"""
    
    st.markdown("## 🔄 Bulk Operations")
    
    bulk_tabs = st.tabs(["📤 Bulk Import", "🧹 Data Cleanup", "📋 Backup & Restore"])
    
    with bulk_tabs[0]:
        st.markdown("### 📤 Bulk Import from CSV")
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown("**Preview:**")
                st.dataframe(df.head())
                
                table_target = st.selectbox("Target Table:", ["players", "matches", "teams", "venues"])
                
                if st.button("Import Data"):
                    # Implementation for bulk import
                    st.info("Bulk import functionality - map CSV columns to database fields")
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
    
    with bulk_tabs[1]:
        st.markdown("### 🧹 Data Cleanup")
        st.info("Remove duplicates, fix data quality issues")
        
        if st.button("Find Duplicate Players"):
            duplicate_query = """
            SELECT name, country, COUNT(*) as count 
            FROM players 
            GROUP BY name, country 
            HAVING COUNT(*) > 1
            """
            duplicates = db.execute_query(duplicate_query)
            if not duplicates.empty:
                st.dataframe(duplicates)
            else:
                st.success("No duplicate players found!")
    
    with bulk_tabs[2]:
        st.markdown("### 📋 Backup & Restore")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Create Backup"):
                success = db.backup_database()
                if success:
                    st.success("✅ Database backup created successfully!")
                else:
                    st.error("❌ Backup failed")
        
        with col2:
            st.info("Restore functionality - upload backup file to restore database")