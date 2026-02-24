import streamlit as st

st.set_page_config(page_title="Prob Model", layout="wide")
st.title("Loading model...")
import streamlit as st
try:
    from model import calculate_all_markets
except Exception as e:
    st.error(f"Model failed to load: {e}")

st.title("Football Probability + Fair Odds Calculator")

home_xg = st.number_input("Home xG (home)", 0.0, 3.5, 1.4)
home_xga = st.number_input("Home xGA (home)", 0.0, 3.5, 1.1)
away_xg = st.number_input("Away xG (away)", 0.0, 3.5, 1.2)
away_xga = st.number_input("Away xGA (away)", 0.0, 3.5, 1.3)
league_avg = st.number_input("League average goals", 1.5, 3.5, 2.4)

if st.button("Calculate"):
    result = calculate_match(home_xg, home_xga, away_xg, away_xga, league_avg)

    st.subheader("Match xG")
    st.write(result["home_xg"], result["away_xg"], "Total:", result["total_xg"])

    st.subheader("Markets")
    st.json(result["markets"])
