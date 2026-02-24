import streamlit as st
from model import calculate_all_markets

st.set_page_config(page_title="Football Probability Model", layout="wide")

st.title("⚽ Football Probability Model")

st.sidebar.header("Input Data")

home_xg = st.sidebar.number_input("Home xG", min_value=0.0, value=1.5, step=0.1)
away_xg = st.sidebar.number_input("Away xG", min_value=0.0, value=1.2, step=0.1)
league_avg = st.sidebar.number_input("League Avg Goals", min_value=0.0, value=2.5, step=0.1)

if st.sidebar.button("Calculate"):

    try:
        results = calculate_all_markets(home_xg, away_xg, league_avg)

        st.subheader("📊 Market Probabilities & Fair Odds")

        for market, (prob, odds) in results.items():
            col1, col2, col3 = st.columns([3, 2, 2])

            col1.write(market)
            col2.write(f"{prob*100:.2f}%")
            col3.write(f"{odds:.2f}")

    except Exception as e:
        st.error(f"Model failed to load: {e}")
