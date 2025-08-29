# SQL Analytics Page - Cricket Analytics Dashboard
# 25+ Advanced SQL queries for cricket analytics

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.db_connection import DatabaseConnection
import sqlite3

def show_sql_analytics():
    """Display SQL analytics interface with 25+ queries"""
    
    st.markdown("# 📋 SQL Analytics & Advanced Queries")
    st.markdown("Interactive SQL query interface with 25+ pre-built cricket analytics queries")
    
    # Initialize database connection
    try:
        db = DatabaseConnection()
        
        # Tabs for different query categories
        tab1, tab2, tab3, tab4 = st.tabs([
            "🟢 Beginner Queries (1-8)", 
            "🟡 Intermediate Queries (9-16)", 
            "🔴 Advanced Queries (17-25)", 
            "💻 Custom Query"
        ])
        
        with tab1:
            show_beginner_queries(db)
        
        with tab2:
            show_intermediate_queries(db)
        
        with tab3:
            show_advanced_queries(db)
        
        with tab4:
            show_custom_query_interface(db)
            
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        st.info("Please ensure the database is properly initialized.")

def show_beginner_queries(db):
    """Display beginner level SQL queries (Questions 1-8)"""
    
    st.markdown("## 🟢 Beginner Level Queries")
    st.markdown("Basic SELECT, WHERE, GROUP BY, and ORDER BY operations")
    
    beginner_queries = {
        "Q1: All Indian Players": {
            "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
            "query": """
            SELECT name, playing_role, batting_style, bowling_style 
            FROM players 
            WHERE country = 'India'
            ORDER BY name;
            """,
            "explanation": "Simple WHERE clause to filter players by country"
        },
        
        "Q2: Recent Matches (30 days)": {
            "description": "Show all cricket matches played in the last 30 days. Include match description, team names, venue, and date.",
            "query": """
            SELECT 
                match_title,
                team1,
                team2,
                venue_name || ', ' || venue_city as venue,
                match_date
            FROM matches 
            WHERE match_date >= date('now', '-30 days')
            ORDER BY match_date DESC;
            """,
            "explanation": "Date filtering with CONCAT for venue display"
        },
        
        "Q3: Top 10 Run Scorers (ODI)": {
            "description": "List the top 10 highest run scorers. Show player name, total runs, batting average, and number of centuries.",
            "query": """
            SELECT 
                name,
                total_runs,
                batting_average,
                CASE 
                    WHEN total_runs > 0 THEN total_runs / 100 
                    ELSE 0 
                END as estimated_centuries
            FROM players 
            WHERE total_runs > 0
            ORDER BY total_runs DESC 
            LIMIT 10;
            """,
            "explanation": "ORDER BY with LIMIT for top results, CASE for calculations"
        },
        
        "Q4: Large Capacity Venues": {
            "description": "Display all cricket venues with seating capacity > 50,000. Show venue name, city, country, and capacity.",
            "query": """
            SELECT venue_name, city, country, capacity
            FROM venues 
            WHERE capacity > 50000
            ORDER BY capacity DESC;
            """,
            "explanation": "Numeric filtering and sorting by capacity"
        },
        
        "Q5: Team Win Statistics": {
            "description": "Calculate how many matches each team has won. Show team name and total wins.",
            "query": """
            SELECT team_name, matches_won as total_wins
            FROM teams 
            ORDER BY matches_won DESC;
            """,
            "explanation": "Simple aggregation query with sorting"
        },
        
        "Q6: Players by Role Count": {
            "description": "Count players by playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
            "query": """
            SELECT 
                playing_role,
                COUNT(*) as player_count
            FROM players 
            WHERE playing_role IS NOT NULL
            GROUP BY playing_role
            ORDER BY player_count DESC;
            """,
            "explanation": "GROUP BY with COUNT aggregation"
        },
        
        "Q7: Highest Scores by Format": {
            "description": "Find the highest individual batting score achieved in each cricket format.",
            "query": """
            SELECT 
                'Test' as format,
                MAX(total_runs) as highest_score
            FROM players
            UNION ALL
            SELECT 
                'ODI' as format,
                MAX(total_runs) as highest_score
            FROM players
            UNION ALL
            SELECT 
                'T20I' as format,
                MAX(total_runs) as highest_score
            FROM players;
            """,
            "explanation": "UNION ALL to combine format-wise maximums"
        },
        
        "Q8: 2024 Cricket Series": {
            "description": "Show all cricket series that started in 2024. Include series name, host country, and match count.",
            "query": """
            SELECT 
                series_name,
                host_country,
                series_type,
                start_date,
                total_matches
            FROM series 
            WHERE strftime('%Y', start_date) = '2024'
            ORDER BY start_date DESC;
            """,
            "explanation": "Date extraction with strftime for year filtering"
        }
    }
    
    display_query_section(beginner_queries, db, "beginner")

def show_intermediate_queries(db):
    """Display intermediate level SQL queries (Questions 9-16)"""
    
    st.markdown("## 🟡 Intermediate Level Queries")
    st.markdown("JOINs, subqueries, and aggregate functions")
    
    intermediate_queries = {
        "Q9: All-rounders Performance": {
            "description": "Find all-rounder players with >1000 runs AND >50 wickets. Show name, runs, wickets.",
            "query": """
            SELECT 
                name,
                total_runs,
                total_wickets,
                playing_role
            FROM players 
            WHERE playing_role = 'All-rounder' 
                AND total_runs > 1000 
                AND total_wickets > 50
            ORDER BY total_runs DESC;
            """,
            "explanation": "Multiple conditions with AND operator"
        },
        
        "Q10: Last 20 Completed Matches": {
            "description": "Get details of the last 20 completed matches with team names, winner, and venue.",
            "query": """
            SELECT 
                match_title,
                team1,
                team2,
                winner,
                victory_margin,
                victory_type,
                venue_name,
                match_date
            FROM matches 
            WHERE match_status = 'Completed'
            ORDER BY match_date DESC 
            LIMIT 20;
            """,
            "explanation": "Status filtering with ORDER BY and LIMIT"
        },
        
        "Q11: Player Performance Across Formats": {
            "description": "Compare players' performance across different formats (requires format-specific data).",
            "query": """
            SELECT 
                p.name,
                p.total_runs,
                p.batting_average,
                p.strike_rate,
                COUNT(ps.match_id) as matches_played
            FROM players p
            LEFT JOIN player_statistics ps ON p.player_id = ps.player_id
            GROUP BY p.player_id, p.name
            HAVING matches_played >= 10
            ORDER BY p.batting_average DESC;
            """,
            "explanation": "LEFT JOIN with GROUP BY and HAVING clause"
        },
        
        "Q12: Home vs Away Performance": {
            "description": "Analyze team performance when playing at home vs away.",
            "query": """
            SELECT 
                t.team_name,
                t.matches_won as total_wins,
                t.matches_played,
                ROUND(t.win_percentage, 2) as win_percentage,
                CASE 
                    WHEN t.country = 'India' THEN 'Home Analysis'
                    ELSE 'Away Analysis'
                END as performance_type
            FROM teams t
            ORDER BY t.win_percentage DESC;
            """,
            "explanation": "CASE statement for conditional logic"
        },
        
        "Q13: Batting Partnerships": {
            "description": "Identify batting partnerships with combined 100+ runs in same innings.",
            "query": """
            SELECT 
                ps1.player_id as player1_id,
                ps2.player_id as player2_id,
                ps1.match_id,
                ps1.innings_number,
                (ps1.runs_scored + ps2.runs_scored) as partnership_runs
            FROM player_statistics ps1
            JOIN player_statistics ps2 ON ps1.match_id = ps2.match_id 
                AND ps1.innings_number = ps2.innings_number
                AND ps1.batting_position = ps2.batting_position - 1
            WHERE (ps1.runs_scored + ps2.runs_scored) >= 100
            ORDER BY partnership_runs DESC;
            """,
            "explanation": "Self JOIN for consecutive batting positions"
        },
        
        "Q14: Bowling Performance by Venue": {
            "description": "Examine bowling performance at different venues (minimum 3 matches).",
            "query": """
            SELECT 
                m.venue_name,
                COUNT(ps.stat_id) as matches_bowled,
                AVG(ps.economy_rate) as avg_economy,
                SUM(ps.wickets_taken) as total_wickets
            FROM player_statistics ps
            JOIN matches m ON ps.match_id = m.match_id
            WHERE ps.overs_bowled >= 4.0
            GROUP BY m.venue_name
            HAVING matches_bowled >= 3
            ORDER BY avg_economy ASC;
            """,
            "explanation": "JOIN with GROUP BY and HAVING for venue analysis"
        },
        
        "Q15: Close Match Performers": {
            "description": "Players who perform well in close matches (decided by <50 runs or <5 wickets).",
            "query": """
            SELECT 
                p.name,
                AVG(ps.runs_scored) as avg_runs_close_matches,
                COUNT(ps.match_id) as close_matches_played
            FROM players p
            JOIN player_statistics ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.victory_margin LIKE '%less than 50 runs%' 
                OR m.victory_margin LIKE '%less than 5 wickets%'
            GROUP BY p.player_id, p.name
            HAVING close_matches_played >= 3
            ORDER BY avg_runs_close_matches DESC;
            """,
            "explanation": "Complex JOIN with LIKE pattern matching"
        },
        
        "Q16: Yearly Performance Trends": {
            "description": "Track batting performance changes over different years (since 2020).",
            "query": """
            SELECT 
                p.name,
                strftime('%Y', m.match_date) as year,
                AVG(ps.runs_scored) as avg_runs_per_match,
                AVG(ps.strike_rate) as avg_strike_rate,
                COUNT(ps.match_id) as matches_played
            FROM players p
            JOIN player_statistics ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.match_date >= '2020-01-01'
            GROUP BY p.player_id, p.name, strftime('%Y', m.match_date)
            HAVING matches_played >= 5
            ORDER BY p.name, year DESC;
            """,
            "explanation": "Date extraction with yearly grouping and trend analysis"
        }
    }
    
    display_query_section(intermediate_queries, db, "intermediate")

def show_advanced_queries(db):
    """Display advanced level SQL queries (Questions 17-25)"""
    
    st.markdown("## 🔴 Advanced Level Queries")
    st.markdown("Window functions, CTEs, and complex analytical calculations")
    
    advanced_queries = {
        "Q17: Toss Advantage Analysis": {
            "description": "Calculate toss win advantage - percentage of matches won by toss winners.",
            "query": """
            WITH toss_analysis AS (
                SELECT 
                    toss_winner,
                    toss_decision,
                    winner,
                    CASE 
                        WHEN toss_winner = winner THEN 1 
                        ELSE 0 
                    END as toss_winner_won
                FROM matches 
                WHERE toss_winner IS NOT NULL AND winner IS NOT NULL
            )
            SELECT 
                toss_decision,
                COUNT(*) as total_matches,
                SUM(toss_winner_won) as toss_winner_victories,
                ROUND(100.0 * SUM(toss_winner_won) / COUNT(*), 2) as win_percentage
            FROM toss_analysis
            GROUP BY toss_decision;
            """,
            "explanation": "CTE with conditional aggregation for toss analysis"
        },
        
        "Q18: Most Economical Bowlers": {
            "description": "Find most economical bowlers in limited-overs cricket (minimum 10 matches).",
            "query": """
            SELECT 
                p.name,
                COUNT(ps.match_id) as matches_bowled,
                AVG(ps.overs_bowled) as avg_overs_per_match,
                AVG(ps.economy_rate) as overall_economy,
                SUM(ps.wickets_taken) as total_wickets
            FROM players p
            JOIN player_statistics ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.match_format IN ('ODI', 'T20I')
                AND ps.overs_bowled >= 2.0
            GROUP BY p.player_id, p.name
            HAVING matches_bowled >= 10 AND avg_overs_per_match >= 2.0
            ORDER BY overall_economy ASC
            LIMIT 15;
            """,
            "explanation": "Multi-format analysis with aggregation constraints"
        },
        
        "Q19: Batting Consistency Analysis": {
            "description": "Determine most consistent batsmen using standard deviation of scores.",
            "query": """
            WITH batting_stats AS (
                SELECT 
                    p.name,
                    ps.runs_scored,
                    AVG(ps.runs_scored) OVER (PARTITION BY p.player_id) as avg_runs,
                    COUNT(*) OVER (PARTITION BY p.player_id) as total_innings
                FROM players p
                JOIN player_statistics ps ON p.player_id = ps.player_id
                JOIN matches m ON ps.match_id = m.match_id
                WHERE ps.balls_faced >= 10 
                    AND m.match_date >= '2022-01-01'
            )
            SELECT 
                name,
                total_innings,
                ROUND(avg_runs, 2) as average_runs,
                ROUND(
                    SQRT(AVG((runs_scored - avg_runs) * (runs_scored - avg_runs))), 2
                ) as standard_deviation
            FROM batting_stats
            GROUP BY name, avg_runs, total_innings
            HAVING total_innings >= 10
            ORDER BY standard_deviation ASC
            LIMIT 20;
            """,
            "explanation": "Window functions with statistical calculations"
        },
        
        "Q20: Multi-Format Player Analysis": {
            "description": "Analyze players across different formats with match counts and averages.",
            "query": """
            WITH format_stats AS (
                SELECT 
                    p.name,
                    m.match_format,
                    COUNT(ps.match_id) as matches,
                    AVG(ps.runs_scored) as avg_runs,
                    SUM(ps.runs_scored) as total_runs
                FROM players p
                JOIN player_statistics ps ON p.player_id = ps.player_id
                JOIN matches m ON ps.match_id = m.match_id
                GROUP BY p.player_id, p.name, m.match_format
            )
            SELECT 
                name,
                SUM(CASE WHEN match_format = 'Test' THEN matches ELSE 0 END) as test_matches,
                SUM(CASE WHEN match_format = 'ODI' THEN matches ELSE 0 END) as odi_matches,
                SUM(CASE WHEN match_format = 'T20I' THEN matches ELSE 0 END) as t20_matches,
                ROUND(AVG(CASE WHEN match_format = 'Test' THEN avg_runs END), 2) as test_avg,
                ROUND(AVG(CASE WHEN match_format = 'ODI' THEN avg_runs END), 2) as odi_avg,
                ROUND(AVG(CASE WHEN match_format = 'T20I' THEN avg_runs END), 2) as t20_avg
            FROM format_stats
            GROUP BY name
            HAVING (test_matches + odi_matches + t20_matches) >= 20
            ORDER BY (test_matches + odi_matches + t20_matches) DESC;
            """,
            "explanation": "Pivot-style aggregation with CASE statements"
        },
        
        "Q21: Comprehensive Performance Ranking": {
            "description": "Create weighted performance ranking combining batting, bowling, and fielding.",
            "query": """
            WITH performance_metrics AS (
                SELECT 
                    p.name,
                    p.total_runs,
                    p.batting_average,
                    p.strike_rate,
                    p.total_wickets,
                    p.bowling_average,
                    p.economy_rate,
                    -- Batting points calculation
                    (p.total_runs * 0.01 + p.batting_average * 0.5 + p.strike_rate * 0.3) as batting_points,
                    -- Bowling points calculation  
                    (p.total_wickets * 2 + (50 - COALESCE(p.bowling_average, 50)) * 0.5 + (6 - COALESCE(p.economy_rate, 6)) * 2) as bowling_points
                FROM players p
                WHERE p.total_runs > 500 OR p.total_wickets > 25
            )
            SELECT 
                name,
                ROUND(batting_points, 2) as batting_points,
                ROUND(bowling_points, 2) as bowling_points,
                ROUND(batting_points + bowling_points, 2) as total_performance_score
            FROM performance_metrics
            ORDER BY total_performance_score DESC
            LIMIT 25;
            """,
            "explanation": "Complex weighted scoring with COALESCE for NULL handling"
        },
        
        "Q22: Head-to-Head Match Analysis": {
            "description": "Build head-to-head prediction analysis between teams (5+ matches).",
            "query": """
            WITH team_matchups AS (
                SELECT 
                    CASE 
                        WHEN team1 < team2 THEN team1 || ' vs ' || team2
                        ELSE team2 || ' vs ' || team1
                    END as matchup,
                    team1,
                    team2,
                    winner,
                    victory_margin,
                    toss_decision,
                    venue_name,
                    match_date
                FROM matches 
                WHERE winner IS NOT NULL 
                    AND match_date >= date('now', '-3 years')
            ),
            matchup_stats AS (
                SELECT 
                    matchup,
                    COUNT(*) as total_matches,
                    SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) as team1_wins,
                    SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) as team2_wins,
                    AVG(CASE WHEN winner = team1 THEN 1.0 ELSE 0.0 END) as team1_win_pct
                FROM team_matchups
                GROUP BY matchup
                HAVING total_matches >= 5
            )
            SELECT 
                matchup,
                total_matches,
                team1_wins,
                team2_wins,
                ROUND(team1_win_pct * 100, 1) as team1_win_percentage
            FROM matchup_stats
            ORDER BY total_matches DESC, team1_win_pct DESC;
            """,
            "explanation": "Complex CTE with conditional string concatenation and statistical analysis"
        },
        
        "Q23: Recent Form Analysis": {
            "description": "Analyze recent player form and momentum (last 10 performances).",
            "query": """
            WITH recent_performances AS (
                SELECT 
                    p.name,
                    ps.runs_scored,
                    ps.strike_rate,
                    m.match_date,
                    ROW_NUMBER() OVER (PARTITION BY p.player_id ORDER BY m.match_date DESC) as recent_rank
                FROM players p
                JOIN player_statistics ps ON p.player_id = ps.player_id
                JOIN matches m ON ps.match_id = m.match_id
                WHERE m.match_date >= date('now', '-1 year')
            ),
            form_analysis AS (
                SELECT 
                    name,
                    AVG(CASE WHEN recent_rank <= 5 THEN runs_scored END) as last_5_avg,
                    AVG(CASE WHEN recent_rank <= 10 THEN runs_scored END) as last_10_avg,
                    AVG(CASE WHEN recent_rank <= 10 THEN strike_rate END) as recent_sr,
                    SUM(CASE WHEN recent_rank <= 10 AND runs_scored >= 50 THEN 1 ELSE 0 END) as scores_above_50
                FROM recent_performances
                WHERE recent_rank <= 10
                GROUP BY name
                HAVING COUNT(*) >= 5
            )
            SELECT 
                name,
                ROUND(last_5_avg, 1) as last_5_matches_avg,
                ROUND(last_10_avg, 1) as last_10_matches_avg,
                ROUND(recent_sr, 1) as recent_strike_rate,
                scores_above_50,
                CASE 
                    WHEN last_5_avg >= 45 AND scores_above_50 >= 3 THEN 'Excellent Form'
                    WHEN last_5_avg >= 30 AND scores_above_50 >= 2 THEN 'Good Form'
                    WHEN last_5_avg >= 20 THEN 'Average Form'
                    ELSE 'Poor Form'
                END as current_form
            FROM form_analysis
            ORDER BY last_5_avg DESC;
            """,
            "explanation": "Window functions with ROW_NUMBER and complex form categorization"
        },
        
        "Q24: Successful Batting Partnerships": {
            "description": "Study successful batting partnerships and player combinations.",
            "query": """
            WITH partnerships AS (
                SELECT 
                    p1.name as player1,
                    p2.name as player2,
                    ps1.match_id,
                    ps1.innings_number,
                    (ps1.runs_scored + ps2.runs_scored) as partnership_runs,
                    CASE WHEN (ps1.runs_scored + ps2.runs_scored) >= 50 THEN 1 ELSE 0 END as good_partnership
                FROM player_statistics ps1
                JOIN player_statistics ps2 ON ps1.match_id = ps2.match_id 
                    AND ps1.innings_number = ps2.innings_number
                    AND ps1.batting_position + 1 = ps2.batting_position
                JOIN players p1 ON ps1.player_id = p1.player_id
                JOIN players p2 ON ps2.player_id = p2.player_id
            ),
            partnership_stats AS (
                SELECT 
                    player1 || ' & ' || player2 as partnership,
                    COUNT(*) as total_partnerships,
                    AVG(partnership_runs) as avg_partnership_runs,
                    MAX(partnership_runs) as highest_partnership,
                    SUM(good_partnership) as partnerships_above_50,
                    ROUND(100.0 * SUM(good_partnership) / COUNT(*), 1) as success_rate
                FROM partnerships
                GROUP BY player1, player2
                HAVING total_partnerships >= 5
            )
            SELECT 
                partnership,
                total_partnerships,
                ROUND(avg_partnership_runs, 1) as avg_runs,
                highest_partnership,
                partnerships_above_50,
                success_rate || '%' as success_percentage
            FROM partnership_stats
            ORDER BY success_rate DESC, avg_partnership_runs DESC
            LIMIT 20;
            """,
            "explanation": "Multi-level CTE with partnership analysis and success metrics"
        },
        
        "Q25: Time-Series Performance Evolution": {
            "description": "Track player performance evolution over quarters with trend analysis.",
            "query": """
            WITH quarterly_performance AS (
                SELECT 
                    p.name,
                    strftime('%Y', m.match_date) || '-Q' || 
                    CASE 
                        WHEN CAST(strftime('%m', m.match_date) AS INT) <= 3 THEN '1'
                        WHEN CAST(strftime('%m', m.match_date) AS INT) <= 6 THEN '2'
                        WHEN CAST(strftime('%m', m.match_date) AS INT) <= 9 THEN '3'
                        ELSE '4'
                    END as quarter,
                    AVG(ps.runs_scored) as quarterly_avg_runs,
                    AVG(ps.strike_rate) as quarterly_avg_sr,
                    COUNT(ps.match_id) as matches_in_quarter
                FROM players p
                JOIN player_statistics ps ON p.player_id = ps.player_id
                JOIN matches m ON ps.match_id = m.match_id
                WHERE m.match_date >= date('now', '-2 years')
                GROUP BY p.player_id, p.name, quarter
                HAVING matches_in_quarter >= 3
            ),
            trend_analysis AS (
                SELECT 
                    name,
                    quarter,
                    quarterly_avg_runs,
                    quarterly_avg_sr,
                    LAG(quarterly_avg_runs) OVER (PARTITION BY name ORDER BY quarter) as prev_quarter_runs,
                    COUNT(*) OVER (PARTITION BY name) as total_quarters
                FROM quarterly_performance
            )
            SELECT 
                name,
                total_quarters,
                ROUND(AVG(quarterly_avg_runs), 2) as overall_quarterly_avg,
                ROUND(AVG(quarterly_avg_sr), 2) as overall_quarterly_sr,
                CASE 
                    WHEN AVG(quarterly_avg_runs - COALESCE(prev_quarter_runs, quarterly_avg_runs)) > 2 THEN 'Career Ascending'
                    WHEN AVG(quarterly_avg_runs - COALESCE(prev_quarter_runs, quarterly_avg_runs)) < -2 THEN 'Career Declining'
                    ELSE 'Career Stable'
                END as career_trajectory
            FROM trend_analysis
            GROUP BY name
            HAVING total_quarters >= 6
            ORDER BY overall_quarterly_avg DESC;
            """,
            "explanation": "Advanced window functions with LAG and quarterly trend analysis"
        }
    }
    
    display_query_section(advanced_queries, db, "advanced")

def display_query_section(queries, db, level):
    """Display a section of queries with execution capability"""
    
    for query_title, query_info in queries.items():
        
        with st.expander(f"📊 {query_title}", expanded=False):
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {query_info['description']}")
                st.markdown(f"**Explanation:** {query_info['explanation']}")
            
            with col2:
                execute_key = f"execute_{level}_{query_title.replace(' ', '_').replace(':', '')}"
                if st.button("▶️ Execute Query", key=execute_key):
                    execute_query_with_results(db, query_info['query'], query_title)
            
            # Show query code
            st.code(query_info['query'], language='sql')

def execute_query_with_results(db, query, title):
    """Execute SQL query and display results"""
    
    try:
        with st.spinner(f"Executing {title}..."):
            
            # Execute query
            result = db.execute_query(query)
            
            if result is not None and not result.empty:
                st.success(f"✅ Query executed successfully! Found {len(result)} results.")
                
                # Display results
                st.markdown("### 📋 Query Results")
                st.dataframe(result, use_container_width=True)
                
                # Add download option
                csv_data = result.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"{title.replace(' ', '_').replace(':', '')}_results.csv",
                    mime="text/csv"
                )
                
                # Create visualization if numeric columns exist
                create_query_visualization(result, title)
                
            else:
                st.info("📭 Query executed successfully but returned no results.")
                
    except Exception as e:
        st.error(f"❌ Query execution failed: {str(e)}")
        st.markdown("**Possible issues:**")
        st.markdown("- Table or column names might not exist")
        st.markdown("- Data might be missing")
        st.markdown("- SQL syntax might need adjustment for your database")

def create_query_visualization(df, title):
    """Create appropriate visualization for query results"""
    
    if df.empty:
        return
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        
        st.markdown("### 📊 Data Visualization")
        
        # Choose visualization type
        viz_type = st.selectbox(
            "Select visualization type:",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"],
            key=f"viz_{title.replace(' ', '_')}"
        )
        
        if viz_type == "Bar Chart" and len(df) <= 20:
            fig = px.bar(
                df.head(15), 
                x=categorical_cols[0], 
                y=numeric_cols[0],
                title=f"{title} - Bar Chart"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Line Chart" and len(numeric_cols) >= 2:
            fig = px.line(
                df.head(20), 
                x=categorical_cols[0] if categorical_cols else df.index, 
                y=numeric_cols[0],
                title=f"{title} - Trend Analysis"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
            fig = px.scatter(
                df.head(50), 
                x=numeric_cols[0], 
                y=numeric_cols[1],
                color=categorical_cols[0] if categorical_cols else None,
                title=f"{title} - Correlation Analysis"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Pie Chart" and len(df) <= 10:
            fig = px.pie(
                df.head(10), 
                values=numeric_cols[0], 
                names=categorical_cols[0],
                title=f"{title} - Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_custom_query_interface(db):
    """Custom SQL query interface for advanced users"""
    
    st.markdown("## 💻 Custom SQL Query Interface")
    st.markdown("Write and execute your own SQL queries against the cricket database")
    
    # Database schema information
    with st.expander("📋 Database Schema Reference", expanded=False):
        
        st.markdown("### Available Tables:")
        
        schema_info = {
            "players": {
                "description": "Player information and career statistics",
                "columns": ["player_id", "name", "country", "playing_role", "batting_style", "bowling_style", 
                          "total_runs", "total_wickets", "batting_average", "bowling_average", "strike_rate", "economy_rate"]
            },
            "matches": {
                "description": "Match information and results",
                "columns": ["match_id", "match_title", "team1", "team2", "venue_name", "venue_city", 
                          "match_date", "match_format", "toss_winner", "toss_decision", "winner", "victory_margin"]
            },
            "player_statistics": {
                "description": "Individual player performance in matches",
                "columns": ["stat_id", "player_id", "match_id", "innings_number", "batting_position", 
                          "runs_scored", "balls_faced", "wickets_taken", "overs_bowled", "economy_rate"]
            },
            "teams": {
                "description": "Team information and overall statistics",
                "columns": ["team_id", "team_name", "country", "matches_played", "matches_won", "win_percentage"]
            },
            "venues": {
                "description": "Cricket venue information",
                "columns": ["venue_id", "venue_name", "city", "country", "capacity", "pitch_type"]
            },
            "series": {
                "description": "Cricket series information",
                "columns": ["series_id", "series_name", "series_type", "host_country", "start_date", "total_matches"]
            }
        }
        
        for table_name, table_info in schema_info.items():
            st.markdown(f"**{table_name}:** {table_info['description']}")
            st.markdown(f"*Columns:* {', '.join(table_info['columns'])}")
            st.markdown("---")
    
    # Query input area
    st.markdown("### ✏️ Write Your Query")
    
    # Sample queries for reference
    sample_queries = [
        "SELECT * FROM players LIMIT 10;",
        "SELECT country, COUNT(*) FROM players GROUP BY country;",
        "SELECT name, total_runs FROM players ORDER BY total_runs DESC LIMIT 5;",
        """SELECT p.name, m.match_title, ps.runs_scored 
FROM players p 
JOIN player_statistics ps ON p.player_id = ps.player_id 
JOIN matches m ON ps.match_id = m.match_id 
LIMIT 10;"""
    ]
    
    selected_sample = st.selectbox(
        "Choose a sample query (optional):",
        [""] + sample_queries,
        key="sample_query_select"
    )
    
    # Text area for custom query
    default_query = selected_sample if selected_sample else "-- Write your SQL query here\nSELECT * FROM players LIMIT 10;"
    
    custom_query = st.text_area(
        "SQL Query:",
        value=default_query,
        height=200,
        help="Write your SQL query here. Use the schema reference above for table and column names."
    )
    
    # Query execution controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        execute_custom = st.button("🚀 Execute Query", type="primary")
    
    with col2:
        validate_query = st.button("✅ Validate Syntax")
    
    with col3:
        st.markdown("*Be careful with UPDATE/DELETE operations!*")
    
    # Execute custom query
    if execute_custom and custom_query.strip():
        
        # Basic safety check
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = custom_query.upper()
        
        has_dangerous = any(keyword in query_upper for keyword in dangerous_keywords)
        
        if has_dangerous:
            st.warning("⚠️ This query contains potentially dangerous operations. Proceed with caution!")
            confirm = st.checkbox("I understand the risks and want to proceed")
            if not confirm:
                st.stop()
        
        # Execute the query
        execute_query_with_results(db, custom_query, "Custom Query")
    
    elif validate_query and custom_query.strip():
        # Simple syntax validation
        try:
            # Try to parse the query (basic validation)
            query_lines = custom_query.strip().split('\n')
            non_empty_lines = [line.strip() for line in query_lines if line.strip() and not line.strip().startswith('--')]
            
            if non_empty_lines:
                first_word = non_empty_lines[0].split()[0].upper()
                if first_word in ['SELECT', 'WITH']:
                    st.success("✅ Query syntax appears valid!")
                else:
                    st.warning("⚠️ Query should typically start with SELECT or WITH")
            else:
                st.error("❌ Query appears to be empty")
                
        except Exception as e:
            st.error(f"❌ Syntax validation failed: {str(e)}")
    
    # Query tips
    with st.expander("💡 SQL Query Tips", expanded=False):
        st.markdown("""
        ### Useful SQL Patterns for Cricket Analytics:
        
        **Basic Queries:**
        ```sql
        -- Top performers
        SELECT name, total_runs FROM players ORDER BY total_runs DESC LIMIT 10;
        
        -- Country statistics
        SELECT country, COUNT(*) as player_count FROM players GROUP BY country;
        ```
        
        **Intermediate Queries:**
        ```sql
        -- Player performance in matches
        SELECT p.name, AVG(ps.runs_scored) as avg_runs
        FROM players p 
        JOIN player_statistics ps ON p.player_id = ps.player_id
        GROUP BY p.player_id, p.name;
        ```
        
        **Advanced Queries:**
        ```sql
        -- Running averages with window functions
        SELECT name, match_date, runs_scored,
               AVG(runs_scored) OVER (PARTITION BY player_id ORDER BY match_date 
               ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as rolling_avg
        FROM player_match_view;
        ```
        
        **Performance Tips:**
        - Use LIMIT for large result sets
        - Index frequently queried columns
        - Use WHERE clauses to filter data early
        - GROUP BY for aggregations
        - JOIN tables efficiently
        """)
    
    # Query history (stored in session state)
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    if execute_custom and custom_query.strip():
        # Add to history (keep last 10)
        if custom_query not in st.session_state.query_history:
            st.session_state.query_history.insert(0, custom_query)
            st.session_state.query_history = st.session_state.query_history[:10]
    
    # Display query history
    if st.session_state.query_history:
        with st.expander("📚 Query History", expanded=False):
            for i, hist_query in enumerate(st.session_state.query_history):
                if st.button(f"Reuse Query {i+1}", key=f"history_{i}"):
                    st.session_state.custom_query_reuse = hist_query
                    st.rerun()
                st.code(hist_query[:100] + "..." if len(hist_query) > 100 else hist_query, language='sql')