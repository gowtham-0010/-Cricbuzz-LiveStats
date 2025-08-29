# Home Page - Cricket Analytics Dashboard
# Welcome page with project overview and navigation

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.db_connection import DatabaseConnection

def show_home_page():
    """Display the home page with project overview and quick stats"""
    
    # Welcome header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; font-size: 3rem;">🏏 Welcome to Cricket Analytics Dashboard</h1>
        <h3 style="color: #666; margin-top: 1rem;">Your Gateway to Comprehensive Cricket Data Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Project overview section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 📊 Project Overview
        
        **Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard that integrates live data from the 
        Cricbuzz API with a SQL database to create an interactive web application. This platform delivers:
        
        - ⚡ **Real-time match updates** from Cricbuzz API
        - 📊 **Detailed player statistics** across all formats
        - 🔍 **SQL-driven analytics** with 25+ advanced queries
        - 🛠️ **Full CRUD operations** for data management
        - 📈 **Interactive visualizations** and insights
        
        ### 🎯 Key Features
        
        **Live Data Integration**
        - Real-time match scorecards and updates
        - Player performance tracking
        - Team statistics and rankings
        - Series and tournament data
        
        **Advanced Analytics**
        - 25 comprehensive SQL queries (Beginner to Advanced)
        - Performance trend analysis
        - Head-to-head comparisons
        - Statistical modeling and predictions
        
        **Data Management**
        - Complete CRUD operations
        - Database-agnostic design
        - Data validation and integrity
        - Export and backup functionality
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Quick Navigation
        
        Use the sidebar to navigate between different sections:
        
        - **📺 Live Matches**: View real-time match data
        - **🏆 Top Player Stats**: Explore player statistics
        - **📋 SQL Analytics**: Run advanced queries
        - **⚙️ CRUD Operations**: Manage database records
        
        ### 🔧 Setup Required
        
        To access live data features:
        1. Get your RapidAPI key
        2. Subscribe to Cricbuzz Cricket API
        3. Enter API key in sidebar
        
        ### 📚 Resources
        - [Cricbuzz API Documentation](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)
        - [Project GitHub Repository](#)
        - [SQL Query Examples](#)
        """)
    
    # Dashboard metrics
    st.markdown("---")
    st.markdown("## 📊 Dashboard Overview")
    
    # Get database connection and fetch stats
    try:
        db = DatabaseConnection()
        
        # Fetch key metrics
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Players count
            cursor.execute("SELECT COUNT(*) FROM players")
            total_players = cursor.fetchone()[0]
            
            # Teams count
            cursor.execute("SELECT COUNT(*) FROM teams")
            total_teams = cursor.fetchone()[0]
            
            # Venues count
            cursor.execute("SELECT COUNT(*) FROM venues")
            total_venues = cursor.fetchone()[0]
            
            # Matches count
            cursor.execute("SELECT COUNT(*) FROM matches")
            total_matches = cursor.fetchone()[0]
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total Players",
                value=total_players,
                delta="Active in database"
            )
        
        with col2:
            st.metric(
                label="🏏 Teams",
                value=total_teams,
                delta="International teams"
            )
        
        with col3:
            st.metric(
                label="🏟️ Venues",
                value=total_venues,
                delta="Cricket grounds"
            )
        
        with col4:
            st.metric(
                label="📋 Matches",
                value=total_matches,
                delta="Recorded matches"
            )
        
        # Quick stats visualizations
        st.markdown("### 📈 Quick Statistics")
        
        # Player roles distribution
        col1, col2 = st.columns(2)
        
        with col1:
            # Fetch player roles data
            player_roles_query = """
            SELECT playing_role, COUNT(*) as count 
            FROM players 
            GROUP BY playing_role
            ORDER BY count DESC
            """
            roles_data = db.execute_query(player_roles_query)
            
            if not roles_data.empty:
                fig_roles = px.pie(
                    roles_data, 
                    values='count', 
                    names='playing_role',
                    title="Player Roles Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_roles.update_layout(height=400)
                st.plotly_chart(fig_roles, use_container_width=True)
        
        with col2:
            # Country wise players
            country_query = """
            SELECT country, COUNT(*) as player_count 
            FROM players 
            GROUP BY country 
            ORDER BY player_count DESC 
            LIMIT 10
            """
            country_data = db.execute_query(country_query)
            
            if not country_data.empty:
                fig_country = px.bar(
                    country_data,
                    x='country',
                    y='player_count',
                    title="Players by Country (Top 10)",
                    color='player_count',
                    color_continuous_scale='viridis'
                )
                fig_country.update_layout(height=400)
                st.plotly_chart(fig_country, use_container_width=True)
        
        # Recent activity section
        st.markdown("### 📅 Recent Activity")
        
        # Sample recent players added
        recent_players_query = """
        SELECT name, country, playing_role, created_at
        FROM players 
        ORDER BY created_at DESC 
        LIMIT 5
        """
        recent_players = db.execute_query(recent_players_query)
        
        if not recent_players.empty:
            st.markdown("**Recently Added Players:**")
            for _, player in recent_players.iterrows():
                st.markdown(f"- **{player['name']}** ({player['country']}) - {player['playing_role']}")
        
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        st.info("Make sure the database is properly initialized and accessible.")
    
    # Business use cases section
    st.markdown("---")
    st.markdown("## 💼 Business Use Cases")
    
    use_cases = [
        {
            "icon": "📺",
            "title": "Sports Media & Broadcasting",
            "description": "Real-time match updates for commentary teams, player performance analysis for pre-match discussions, and historical data trends for match predictions."
        },
        {
            "icon": "🎮",
            "title": "Fantasy Cricket Platforms",
            "description": "Player form analysis and recent performance tracking, head-to-head statistics for team selection, and real-time score updates for fantasy leagues."
        },
        {
            "icon": "📈",
            "title": "Cricket Analytics Firms",
            "description": "Advanced statistical modeling and player evaluation, performance trend analysis across different formats, and data-driven insights for team management."
        },
        {
            "icon": "🎓",
            "title": "Educational Institutions",
            "description": "Teaching database operations with real-world data, SQL practice with engaging cricket datasets, and API integration learning."
        },
        {
            "icon": "🎲",
            "title": "Sports Betting & Prediction",
            "description": "Historical performance analysis for odds calculation, player form and momentum tracking, and venue-specific performance insights."
        }
    ]
    
    for i in range(0, len(use_cases), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(use_cases):
                use_case = use_cases[i + j]
                with col:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; height: 150px;">
                        <h4>{use_case['icon']} {use_case['title']}</h4>
                        <p style="font-size: 0.9rem; color: #666;">{use_case['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Technology stack
    st.markdown("---")
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Plotly
        - Custom CSS
        """)
    
    with col2:
        st.markdown("""
        **Backend**
        - Python
        - Pandas
        - SQLAlchemy
        """)
    
    with col3:
        st.markdown("""
        **Database**
        - SQLite
        - PostgreSQL
        - MySQL
        """)
    
    with col4:
        st.markdown("""
        **API**
        - Cricbuzz API
        - RapidAPI
        - Requests
        """)
    
    # Getting started section
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    ### Step 1: API Setup
    1. Visit [RapidAPI](https://rapidapi.com/) and create an account
    2. Search for "Cricbuzz Cricket API" and subscribe to the free plan
    3. Copy your API key and enter it in the sidebar
    
    ### Step 2: Explore Features
    - Start with **Live Matches** to see real-time data
    - Check **Top Player Stats** for statistical insights
    - Try **SQL Analytics** for advanced queries
    - Use **CRUD Operations** to manage data
    
    ### Step 3: Advanced Usage
    - Customize SQL queries for specific analysis
    - Export data for external analysis
    - Set up automated data collection
    - Integrate with other cricket data sources
    
    ### Need Help?
    - Check the sidebar for quick navigation tips
    - Visit individual pages for specific documentation
    - Review sample queries in SQL Analytics section
    """)
    
    # Footer with additional information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background-color: #f0f2f6; border-radius: 10px; margin-top: 2rem;">
        <h4>🏏 Ready to Dive Deep into Cricket Analytics?</h4>
        <p>Select a page from the sidebar to begin your cricket data exploration journey!</p>
        <p><em>This dashboard is designed to provide comprehensive cricket analytics for enthusiasts, professionals, and educators.</em></p>
    </div>
    """, unsafe_allow_html=True)