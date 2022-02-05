import streamlit as st

from views.strategy import strategy
from views.season_result import season_result
from views.race_lap_result import race_lap_result
from views.qualify_result import qualify_result


def home():
    st.header("Formula 1 data and strategy")
    st.markdown(
        "This app shows data about FIA Formula 1 world championship and calculates optimal race strategy on the basis of very simple assumption."
    )
    st.markdown(
        "So far, data about drivers championship points, pace graph, and qualifying result of each Grand Prix is available (data source: https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020)."
    )
    st.markdown(
        "Optimal race strategy in this app just shows the fastest tyre combination and how many laps should by completed by each tyre assuming linear tyre degradation without considering other factors (ex. track position)."
    )
    st.markdown("Go to select left side selectbox and use each function!")


def main():
    views = {
        "Home": home,
        "Season result": season_result,
        "Grand prix result (lap time)": race_lap_result,
        "Qualify result": qualify_result,
        "Optimal strategy": strategy,
    }
    selected_views = st.sidebar.selectbox(label="views", options=views.keys())
    render_view = views[selected_views]
    render_view()


if __name__ == "__main__":
    main()
