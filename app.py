import streamlit as st

from views.strategy import strategy
from views.season_result import season_result
from views.race_lap_result import race_lap_result
from views.qualify_result import qualify_result


# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def sr():
    return season_result()


# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def rlr():
    return race_lap_result()


# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def qr():
    return qualify_result()


# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def strat():
    return strategy()


def home():
    st.header("Formula 1 data and strategy")
    st.markdown(
        "This app shows data about FIA Formula 1 world championship and calculates optimal race strategy on the basis of very simple assumption."
    )
    st.markdown(
        "So far, data about drivers championship points, pace graph, and qualifying result of each Grand Prix is available (data source: https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020)."
    )
    st.markdown(
        "Optimal race strategy in this app just shows the fastest tyre combination and how many laps should be completed by each tyre assuming linear tyre degradation without considering other factors (ex. track position)."
    )
    # show each function
    sr()
    rlr()
    qr()
    strat()


def main():
    st.set_page_config(layout="wide")
    views = {
        "Home": home,
        "Season result": season_result,
        "Grand prix result": race_lap_result,
        "Qualify result": qualify_result,
        "Optimal strategy": strategy,
    }
    selected_views = st.sidebar.selectbox(label="views", options=views.keys())
    render_view = views[selected_views]
    render_view()


if __name__ == "__main__":
    main()
