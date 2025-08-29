# Cricket Analytics Dashboard - Main Application
# Cricbuzz LiveStats Project
# Author: Auto-generated Cricket Analytics System

import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.db_connection import DatabaseConnection
from pages.home import show_home_page
from pages.live_matches import show_live_matches
from pages.top_stats import show_top_stats
from pages.sql_queries import show_sql_analytics
from pages.crud_operations import show_crud_operations

# Page configuration
st.set_page_config(
    page_title="Cricket Analytics Dashboard - Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .sidebar-title {
        color: #1f77b4;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🏏 Cricket Analytics Dashboard - Cricbuzz LiveStats</div>', 
                unsafe_allow_html=True)
    
    # Initialize database
    db = DatabaseConnection()
    db.create_tables()
    
    # Sidebar navigation
    st.sidebar.markdown('<div class="sidebar-title">📊 Navigation</div>', unsafe_allow_html=True)
    
    page_options = [
        "🏠 Home",
        "📺 Live Matches",
        "🏆 Top Player Stats",
        "📋 SQL Analytics",
        "⚙️ CRUD Operations"
    ]
    
    selected_page = st.sidebar.selectbox(
        "Select Page",
        options=page_options,
        index=0
    )
    
    # API Configuration section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 API Configuration")
    
    # Store API key in session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    api_key = st.sidebar.text_input(
        "RapidAPI Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your RapidAPI key for Cricbuzz Cricket API"
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
    
    if not api_key:
        st.sidebar.warning("⚠️ Please enter your RapidAPI key to access live data")
        st.sidebar.markdown("""
        **How to get API Key:**
        1. Visit [RapidAPI](https://rapidapi.com/)
        2. Search for "Cricbuzz Cricket"
        3. Subscribe to free plan
        4. Copy your API key
        """)
    
    # Quick Stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    try:
        # Get some quick database stats
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Count players
            cursor.execute("SELECT COUNT(*) FROM players")
            player_count = cursor.fetchone()[0]
            
            # Count matches
            cursor.execute("SELECT COUNT(*) FROM matches")
            match_count = cursor.fetchone()[0]
            
            st.sidebar.metric("Total Players", player_count)
            st.sidebar.metric("Total Matches", match_count)
            
    except Exception as e:
        st.sidebar.error(f"Database connection error: {str(e)}")
    
    # Page routing
    if selected_page == "🏠 Home":
        show_home_page()
    elif selected_page == "📺 Live Matches":
        show_live_matches(api_key)
    elif selected_page == "🏆 Top Player Stats":
        show_top_stats(api_key)
    elif selected_page == "📋 SQL Analytics":
        show_sql_analytics()
    elif selected_page == "⚙️ CRUD Operations":
        show_crud_operations()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🏏 Cricket Analytics Dashboard | Built with Streamlit & Python | 
        Data Source: Cricbuzz API | © 2025 Cricbuzz LiveStats</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()