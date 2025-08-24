import streamlit as st
import requests

# Your RapidAPI key
API_KEY = "f0beadeebbmsh58a7273cdf0621bp1187dejsnc7cb81759c22"
API_HOST = "cricbuzz-cricket.p.rapidapi.com"
LIVE_MATCHES_URL = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

st.title("Live Cricket Matches")

def fetch_live_matches():
    try:
        response = requests.get(LIVE_MATCHES_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Could not fetch live matches: {e}")
        return None

data = fetch_live_matches()

if data and "typeMatches" in data and len(data["typeMatches"]) > 0:
    series_matches = data["typeMatches"][0].get("seriesMatches", [])
    if series_matches and len(series_matches) > 0:
        series_ad_wrapper = series_matches[0].get("seriesAdWrapper", {})
        matches = series_ad_wrapper.get("matches", [])
        for idx, match in enumerate(matches):
            info = match.get("matchInfo", {})
            st.subheader(info.get("matchDesc", "Match Info"))
            team1 = info.get("team1", {}).get("teamName", "N/A")
            team2 = info.get("team2", {}).get("teamName", "N/A")
            st.write(f"Teams: {team1} vs {team2}")
            st.write(f"Status: {info.get('status', 'N/A')}")
            st.write(f"Venue: {info.get('venueInfo', {}).get('ground', 'N/A')}")

            button_key = f"scorecard_button_{idx}"
            if st.button(f"Show Scorecard for {info.get('matchDesc')}", key=button_key):
                match_id = info.get("id")
                if match_id:
                    scorecard_url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/{match_id}/scorecard"
                    try:
                        score_resp = requests.get(scorecard_url, headers=headers, timeout=10)
                        score_resp.raise_for_status()
                        scorecard = score_resp.json()
                        st.json(scorecard)
                    except Exception as e:
                        st.error(f"Error fetching scorecard: {e}")
    else:
        st.info("No series matches found.")
else:
    st.info("No live matches currently available.")
