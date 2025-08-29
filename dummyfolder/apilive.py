import streamlit as st
from live_matches import live_matches   # replace with your file name

st.title("🏏 Test Live Matches Page")

df = live_matches()

if df is None or df.empty:
    st.warning("⚠️ No live matches found (check API key or endpoint).")
else:
    st.success("✅ Live matches fetched!")
    st.dataframe(df.head())  # show first few rows
