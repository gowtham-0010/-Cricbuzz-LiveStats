import streamlit as st
from utils.db_connection import create_connection

def main():
    st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏")
    st.title("Cricbuzz LiveStats: Real-Time Cricket Insights")

    st.write("Welcome to the Cricbuzz analytics dashboard.")

    # Connect to database
    connection = create_connection()
    if connection:
        st.success("Connected to MySQL Database successfully!")
        connection.close()
    else:
        st.error("Failed to connect to the database.")
    
if __name__ == "__main__":
    main()
