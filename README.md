# Cricket Analytics Dashboard - Cricbuzz LiveStats

A comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with a SQL database to create an interactive web application delivering real-time match updates, detailed player statistics, and advanced analytics.

## 🏗️ Project Structure

```
cricbuzz_livestats/
├── app.py                    # Main entry point for the Streamlit app
├── requirements.txt          # Required Python packages
├── README.md                # Project overview and setup instructions
├── pages/                   # Contains individual Streamlit pages
│   ├── home.py             # Overview and About the Project page
│   ├── live_matches.py     # Displays live match data from Cricbuzz API
│   ├── top_stats.py        # Shows top batting/bowling stats
│   ├── sql_queries.py      # SQL query interface and analytics
│   └── crud_operations.py  # Perform CRUD on player stats
├── utils/                   # Utility files
│   └── db_connection.py    # SQL database connection logic
└── notebooks/              # Practice Jupyter notebooks (Optional)
    └── data_fetching.ipynb # For testing API calls and pushing to DB
```

## ⚡ Features

### 🌐 API Integration
- Real-time data fetching from Cricbuzz Cricket API via RapidAPI
- Live match updates and scorecards
- Player statistics and series information
- Error handling and rate limiting

### 🖥️ Interactive Dashboard
- Multi-page web application using Streamlit
- Live scorecards and statistics visualization
- Custom SQL query interface with 25+ pre-built analytics queries
- Administrative CRUD operations with form-based UI

### 🗄️ SQL Database Integration
- Database-agnostic design (PostgreSQL, MySQL, SQLite)
- Centralized connection handling
- Optimized queries for performance
- Sample data initialization

### ⚙️ CRUD Operations
- Add, update, and delete player records
- Match statistics management
- Data validation and integrity checks
- Bulk operations support

## 💼 Business Use Cases

1. **📺 Sports Media & Broadcasting**
   - Real-time match updates for commentary teams
   - Player performance analysis for pre-match discussions
   - Historical data trends for match predictions

2. **🎮 Fantasy Cricket Platforms**
   - Player form analysis and recent performance tracking
   - Head-to-head statistics for team selection
   - Real-time score updates for fantasy leagues

3. **📈 Cricket Analytics Firms**
   - Advanced statistical modeling and player evaluation
   - Performance trend analysis across different formats
   - Data-driven insights for team management

4. **🎓 Educational Institutions**
   - Teaching database operations with real-world data
   - SQL practice with engaging cricket datasets
   - API integration and web development learning

5. **🎲 Sports Betting & Prediction**
   - Historical performance analysis for odds calculation
   - Player form and momentum tracking
   - Venue-specific performance insights

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- RapidAPI account with Cricbuzz Cricket API access
- Database system (SQLite, PostgreSQL, or MySQL)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd cricbuzz_livestats
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: API Configuration
1. Visit [RapidAPI](https://rapidapi.com/)
2. Search for "Cricbuzz Cricket API"
3. Subscribe to the free plan
4. Copy your API key
5. Enter the API key in the sidebar when running the application

### Step 4: Database Setup
The application will automatically create SQLite database tables. For other databases:

**PostgreSQL:**
```python
# Update utils/db_connection.py with your credentials
DATABASE_URL = "postgresql://username:password@localhost:5432/cricket_db"
```

**MySQL:**
```python
# Update utils/db_connection.py with your credentials
DATABASE_URL = "mysql://username:password@localhost:3306/cricket_db"
```

### Step 5: Run Application
```bash
streamlit run app.py
```

## 📊 SQL Analytics Queries

The dashboard includes 25 comprehensive SQL queries categorized by difficulty:

### Beginner Level (1-8)
- Player statistics by country
- Recent matches analysis
- Top run scorers and wicket takers
- Venue capacity analysis
- Team win statistics

### Intermediate Level (9-16)
- All-rounder performance analysis
- Format-wise player comparisons
- Home vs away team performance
- Batting partnerships analysis
- Close matches performance tracking

### Advanced Level (17-25)
- Toss advantage analysis
- Player consistency metrics
- Performance ranking systems
- Head-to-head predictions
- Time-series performance evolution

## 📱 Pages Overview

### 🏠 Home Page
- Project description and navigation guide
- Quick statistics dashboard
- Recent activity summary
- API status indicators

### 📺 Live Matches Page
- Real-time match scorecards
- Live player statistics
- Match venue and conditions
- Ball-by-ball commentary integration

### 🏆 Top Player Stats Page
- Leading run scorers across formats
- Top wicket takers and bowling figures
- All-rounder performances
- Format-wise statistical leaders

### 📋 SQL Analytics Page
- Interactive query execution interface
- 25+ pre-built analytical queries
- Custom query builder
- Data export functionality

### ⚙️ CRUD Operations Page
- Player data management forms
- Match statistics entry
- Bulk data operations
- Data validation and error handling

## 🛠️ Technical Architecture

### Frontend
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualizations
- **Custom CSS**: Enhanced UI styling

### Backend
- **Python**: Core application logic
- **SQLAlchemy**: Database ORM
- **Pandas**: Data manipulation and analysis

### Database Schema
```sql
-- Players table
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    playing_role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Matches table
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    venue VARCHAR(200),
    match_date DATE,
    match_format VARCHAR(20),
    result VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Additional tables for comprehensive analytics...
```

### API Integration
- **Cricbuzz Cricket API**: Live data source
- **Request handling**: Error management and retries
- **Rate limiting**: API call optimization
- **Caching**: Performance improvements

## 🎯 Key Features Implementation

### Real-time Data Updates
```python
# Auto-refresh mechanism for live data
if st.button("🔄 Refresh Live Data"):
    with st.spinner("Fetching latest data..."):
        live_data = fetch_live_matches(api_key)
        st.success("Data updated successfully!")
```

### Interactive Visualizations
```python
# Dynamic charts with Plotly
fig = px.bar(data, x='player_name', y='runs', 
             title='Top Run Scorers')
st.plotly_chart(fig, use_container_width=True)
```

### Advanced SQL Analytics
```python
# Custom query execution
query_result = execute_custom_query(user_query)
st.dataframe(query_result)
st.download_button("Download CSV", 
                   query_result.to_csv())
```

## 📈 Performance Optimization

- **Database indexing** on frequently queried columns
- **Connection pooling** for database efficiency
- **Caching mechanisms** for API responses
- **Lazy loading** for large datasets
- **Query optimization** for complex analytics

## 🔒 Security Features

- **API key encryption** and secure storage
- **SQL injection protection** through parameterized queries
- **Input validation** for all user inputs
- **Error logging** and monitoring
- **Rate limiting** for API calls

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v --cov=.
```

## 📚 Documentation

Each module includes comprehensive docstrings and inline comments. For detailed API documentation, refer to the individual page modules.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Check the documentation
- Review the FAQ section

## 🏏 Happy Cricket Analytics!

Start exploring cricket data like never before with this comprehensive analytics dashboard!