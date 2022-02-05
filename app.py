import streamlit as st

from views.strategy import strategy
from views.season_result import season_result
from views.race_lap_result import race_lap_result


def home():
    st.header("Formula 1 data and strategy")


def main():
    views = {
        "Home": home,
        "Season result": season_result,
        "Grand prix result (lap time)": race_lap_result,
        "Optimal strategy": strategy,
    }
    selected_views = st.sidebar.selectbox(label="views", options=views.keys())
    render_view = views[selected_views]
    render_view()


if __name__ == "__main__":
    main()
