import streamlit as st

from views.strategy import strategy
from views.season_result import season_result
from views.race_lap_result import race_lap_result
from views.qualify_result import qualify_result


def display_season_result():
    """Display season result view."""
    return season_result()


def display_race_lap_result():
    """Display race lap result view."""
    return race_lap_result()


def display_qualify_result():
    """Display qualifying result view."""
    return qualify_result()


def display_strategy():
    """Display strategy view."""
    return strategy()


def home():
    """Display home page."""
    st.header("Formula 1 Data and Strategy Analysis")
    st.markdown(
        "This app provides insights into the FIA Formula 1 World Championship and calculates optimal race strategies based on simple assumptions."
    )
    st.markdown(
        "Currently, the app offers data on driver championship points, pace graphs, and qualifying results for each Grand Prix. The data source is [Kaggle](https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020)."
    )
    st.markdown(
        "The optimal race strategy feature displays the fastest tire combination and suggests the number of laps to be completed on each tire. This is calculated assuming linear tire degradation and does not take into account other factors such as track position."
    )
    # Display each view
    display_season_result()
    display_race_lap_result()
    display_qualify_result()
    display_strategy()


def main():
    """Main function."""
    st.set_page_config(layout="wide")
    views = {
        "Home": home,
        "Season Results": display_season_result,
        "Grand Prix Results": display_race_lap_result,
        "Qualifying Results": display_qualify_result,
        "Optimal Strategy": display_strategy,
    }
    selected_view = st.sidebar.selectbox(label="Views", options=list(views.keys()))
    render_view = views[selected_view]
    render_view()


if __name__ == "__main__":
    main()
