
# Database Connection Handler
# Centralized database connectivity for Cricket Analytics Dashboard

import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from contextlib import contextmanager
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Database connection handler supporting multiple database types
    Supports SQLite, PostgreSQL, and MySQL
    """
    
    def __init__(self, db_type='sqlite', **kwargs):
        """
        Initialize database connection
        
        Args:
            db_type (str): Type of database ('sqlite', 'postgresql', 'mysql')
            **kwargs: Database connection parameters
        """
        self.db_type = db_type
        self.connection_params = kwargs
        
        # Default SQLite configuration
        if db_type == 'sqlite':
            self.db_path = kwargs.get('db_path', 'cricket_analytics.db')
            self.connection_string = f'sqlite:///{self.db_path}'
        
        # PostgreSQL configuration
        elif db_type == 'postgresql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 5432)
            database = kwargs.get('database', 'cricket_db')
            username = kwargs.get('username', 'postgres')
            password = kwargs.get('password', 'password')
            self.connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
        
        # MySQL configuration
        elif db_type == 'mysql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 3306)
            database = kwargs.get('database', 'cricket_db')
            username = kwargs.get('username', 'root')
            password = kwargs.get('password', 'password')
            self.connection_string = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        # Create engine
        try:
            self.engine = create_engine(self.connection_string, echo=False)
            logger.info(f"Database engine created for {db_type}")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Ensures proper connection handling and cleanup
        """
        if self.db_type == 'sqlite':
            conn = sqlite3.connect(self.db_path)
            try:
                yield conn
            finally:
                conn.close()
        else:
            conn = self.engine.connect()
            try:
                yield conn
            finally:
                conn.close()
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute SQL query with optional parameters
        
        Args:
            query (str): SQL query to execute
            params (dict): Query parameters
            fetch (bool): Whether to fetch results
            
        Returns:
            pandas.DataFrame or None: Query results
        """
        try:
            with self.get_connection() as conn:
                if fetch:
                    if params:
                        return pd.read_sql_query(text(query), conn, params=params)
                    else:
                        return pd.read_sql_query(query, conn)
                else:
                    if self.db_type == 'sqlite':
                        cursor = conn.cursor()
                        if params:
                            cursor.execute(query, params)
                        else:
                            cursor.execute(query)
                        conn.commit()
                    else:
                        if params:
                            conn.execute(text(query), params)
                        else:
                            conn.execute(text(query))
                        conn.commit()
                    return None
                    
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def create_tables(self):
        """Create all necessary database tables"""
        
        # Players table
        players_table = """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(50),
            playing_role VARCHAR(50),
            batting_style VARCHAR(50),
            bowling_style VARCHAR(50),
            date_of_birth DATE,
            total_runs INTEGER DEFAULT 0,
            total_wickets INTEGER DEFAULT 0,
            batting_average DECIMAL(5,2) DEFAULT 0.0,
            bowling_average DECIMAL(5,2) DEFAULT 0.0,
            strike_rate DECIMAL(5,2) DEFAULT 0.0,
            economy_rate DECIMAL(4,2) DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Matches table
        matches_table = """
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_title VARCHAR(200) NOT NULL,
            team1 VARCHAR(100) NOT NULL,
            team2 VARCHAR(100) NOT NULL,
            venue_name VARCHAR(200),
            venue_city VARCHAR(100),
            venue_country VARCHAR(50),
            match_date DATE,
            match_format VARCHAR(20),
            toss_winner VARCHAR(100),
            toss_decision VARCHAR(20),
            winner VARCHAR(100),
            victory_margin VARCHAR(100),
            victory_type VARCHAR(50),
            man_of_match VARCHAR(100),
            match_status VARCHAR(50) DEFAULT 'Scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Player statistics table
        player_stats_table = """
        CREATE TABLE IF NOT EXISTS player_statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            match_id INTEGER,
            innings_number INTEGER,
            batting_position INTEGER,
            runs_scored INTEGER DEFAULT 0,
            balls_faced INTEGER DEFAULT 0,
            fours INTEGER DEFAULT 0,
            sixes INTEGER DEFAULT 0,
            strike_rate DECIMAL(5,2),
            overs_bowled DECIMAL(3,1) DEFAULT 0.0,
            wickets_taken INTEGER DEFAULT 0,
            runs_conceded INTEGER DEFAULT 0,
            economy_rate DECIMAL(4,2),
            catches INTEGER DEFAULT 0,
            stumpings INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
        )
        """
        
        # Teams table
        teams_table = """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name VARCHAR(100) UNIQUE NOT NULL,
            country VARCHAR(50),
            team_type VARCHAR(20),
            matches_played INTEGER DEFAULT 0,
            matches_won INTEGER DEFAULT 0,
            matches_lost INTEGER DEFAULT 0,
            matches_tied INTEGER DEFAULT 0,
            win_percentage DECIMAL(5,2) DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Venues table
        venues_table = """
        CREATE TABLE IF NOT EXISTS venues (
            venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            venue_name VARCHAR(200) NOT NULL,
            city VARCHAR(100),
            country VARCHAR(50),
            capacity INTEGER,
            pitch_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Series table
        series_table = """
        CREATE TABLE IF NOT EXISTS series (
            series_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name VARCHAR(200) NOT NULL,
            series_type VARCHAR(50),
            host_country VARCHAR(50),
            start_date DATE,
            end_date DATE,
            total_matches INTEGER DEFAULT 0,
            matches_completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Execute table creation
        tables = [
            players_table,
            matches_table,
            player_stats_table,
            teams_table,
            venues_table,
            series_table
        ]
        
        for table_sql in tables:
            try:
                self.execute_query(table_sql, fetch=False)
                logger.info("Table created successfully")
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        # Insert sample data if tables are empty
        self._insert_sample_data()
    
    def _insert_sample_data(self):
        """Insert sample data for demonstration"""
        
        # Check if data already exists
        try:
            player_count = self.execute_query("SELECT COUNT(*) as count FROM players")
            if player_count.iloc[0]['count'] > 0:
                return  # Data already exists
        except:
            pass  # Continue with sample data insertion
        
        # Sample players data
        sample_players = [
            ('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', 'Right-arm medium', '1988-11-05', 12000, 4, 50.5, 25.0, 92.5, 6.5),
            ('Rohit Sharma', 'India', 'Batsman', 'Right-hand bat', 'Right-arm off-break', '1987-04-30', 9500, 8, 48.2, 20.5, 88.3, 5.8),
            ('Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand bat', 'Right-arm off-break', '1990-08-08', 7800, 12, 47.8, 18.2, 81.2, 4.9),
            ('Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', 'Right-arm leg-break', '1989-06-02', 8200, 17, 61.8, 30.1, 86.4, 4.7),
            ('Babar Azam', 'Pakistan', 'Batsman', 'Right-hand bat', 'Right-arm off-break', '1994-10-15', 4500, 3, 45.9, 33.3, 89.7, 5.2),
            ('Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-12-06', 150, 150, 12.5, 22.1, 65.4, 4.6),
            ('Trent Boult', 'New Zealand', 'Bowler', 'Left-hand bat', 'Left-arm fast-medium', '1989-07-22', 200, 180, 15.8, 27.8, 70.2, 4.8),
            ('Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-05-08', 350, 200, 22.1, 23.4, 75.6, 3.2),
            ('Kagiso Rabada', 'South Africa', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1995-05-25', 180, 170, 18.2, 22.9, 68.8, 4.4),
            ('Rashid Khan', 'Afghanistan', 'Bowler', 'Right-hand bat', 'Right-arm leg-break', '1998-09-20', 220, 120, 11.5, 18.2, 85.4, 6.2),
            ('Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', '1991-06-04', 4800, 95, 35.8, 31.2, 82.1, 3.8),
            ('Shakib Al Hasan', 'Bangladesh', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', '1987-03-24', 6500, 280, 38.9, 31.1, 81.3, 4.9),
            ('Ravindra Jadeja', 'India', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', '1988-12-06', 2500, 220, 35.2, 24.8, 86.5, 2.4),
            ('MS Dhoni', 'India', 'Wicket-keeper', 'Right-hand bat', 'Right-arm medium', '1981-07-07', 10500, 1, 50.6, 0.0, 87.6, 0.0),
            ('Jos Buttler', 'England', 'Wicket-keeper', 'Right-hand bat', None, '1990-09-08', 4200, 0, 41.8, 0.0, 118.4, 0.0)
        ]
        
        # Insert players
        for player in sample_players:
            insert_player_query = """
            INSERT OR IGNORE INTO players 
            (name, country, playing_role, batting_style, bowling_style, date_of_birth, 
             total_runs, total_wickets, batting_average, bowling_average, strike_rate, economy_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                self.execute_query(insert_player_query, player, fetch=False)
            except Exception as e:
                logger.warning(f"Failed to insert player {player[0]}: {e}")
        
        # Sample teams data
        sample_teams = [
            ('India', 'India', 'International', 250, 180, 65, 5, 72.0),
            ('Australia', 'Australia', 'International', 220, 160, 55, 5, 72.7),
            ('England', 'England', 'International', 200, 130, 65, 5, 65.0),
            ('New Zealand', 'New Zealand', 'International', 180, 110, 65, 5, 61.1),
            ('Pakistan', 'Pakistan', 'International', 190, 120, 65, 5, 63.2),
            ('South Africa', 'South Africa', 'International', 170, 100, 65, 5, 58.8),
            ('West Indies', 'West Indies', 'International', 160, 90, 65, 5, 56.3),
            ('Bangladesh', 'Bangladesh', 'International', 140, 70, 65, 5, 50.0),
            ('Sri Lanka', 'Sri Lanka', 'International', 150, 85, 60, 5, 56.7),
            ('Afghanistan', 'Afghanistan', 'International', 100, 45, 50, 5, 45.0)
        ]
        
        # Insert teams
        for team in sample_teams:
            insert_team_query = """
            INSERT OR IGNORE INTO teams 
            (team_name, country, team_type, matches_played, matches_won, 
             matches_lost, matches_tied, win_percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                self.execute_query(insert_team_query, team, fetch=False)
            except Exception as e:
                logger.warning(f"Failed to insert team {team[0]}: {e}")
        
        # Sample venues
        sample_venues = [
            ('Lord\'s Cricket Ground', 'London', 'England', 30000, 'Balanced'),
            ('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024, 'Batting-friendly'),
            ('Eden Gardens', 'Kolkata', 'India', 66349, 'Spin-friendly'),
            ('Wankhede Stadium', 'Mumbai', 'India', 33108, 'Batting-friendly'),
            ('The Oval', 'London', 'England', 25500, 'Balanced'),
            ('Sydney Cricket Ground', 'Sydney', 'Australia', 48000, 'Batting-friendly'),
            ('Dubai International Cricket Stadium', 'Dubai', 'UAE', 25000, 'Batting-friendly'),
            ('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000, 'Batting-friendly'),
            ('Basin Reserve', 'Wellington', 'New Zealand', 11600, 'Bowling-friendly'),
            ('Newlands', 'Cape Town', 'South Africa', 25000, 'Balanced')
        ]
        
        # Insert venues
        for venue in sample_venues:
            insert_venue_query = """
            INSERT OR IGNORE INTO venues 
            (venue_name, city, country, capacity, pitch_type)
            VALUES (?, ?, ?, ?, ?)
            """
            try:
                self.execute_query(insert_venue_query, venue, fetch=False)
            except Exception as e:
                logger.warning(f"Failed to insert venue {venue[0]}: {e}")
        
        logger.info("Sample data inserted successfully")
    
    def test_connection(self):
        """Test database connection"""
        try:
            result = self.execute_query("SELECT 1 as test")
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    def get_table_info(self, table_name):
        """Get table structure information"""
        if self.db_type == 'sqlite':
            query = f"PRAGMA table_info({table_name})"
        elif self.db_type == 'postgresql':
            query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            """
        else:  # MySQL
            query = f"DESCRIBE {table_name}"
        
        return self.execute_query(query)
    
    def backup_database(self, backup_path=None):
        """Create database backup"""
        if self.db_type != 'sqlite':
            logger.warning("Backup only implemented for SQLite databases")
            return False
        
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"cricket_analytics_backup_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False