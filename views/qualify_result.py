import os

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

current_dir = os.path.dirname(__file__)


def _cvt2seconds(t):
    """Convert qualifying time written by string to seconds."""
    if "N" in t or t == "":
        sec = np.nan
    else:  
        if ":" in t:  
            list_tmp = [float(x) if i==1 else float(x)*60 for i, x in enumerate(t.split(":"))]
            sec = list_tmp[0] + list_tmp[1]
        else:
            sec = float(t)
    return sec


def _read_data() -> pd.DataFrame:
    """Read data."""
    df_qualifying = pd.read_csv(
        os.path.join(current_dir, "../data/qualifying.csv"),
        usecols=["driverId", "position", "raceId", "q1", "q2", "q3"], dtype={"q1":str, "q2":str, "q3":str})
    df_drivers = pd.read_csv(os.path.join(current_dir, "../data/drivers.csv"),
                                usecols=["driverId", "driverRef"])
    df_races = pd.read_csv(os.path.join(current_dir, "../data/races.csv"),
                            usecols=["raceId", "name", "round", "year"])
    df = pd.merge(df_qualifying, df_drivers, on=["driverId"], how="left")
    df = pd.merge(df, df_races, on=["raceId"], how="left")
    df.fillna("", inplace=True)
    df.dropna(inplace=True)
    for q in range(1, 4):
        df.insert(len(df.columns), f"q{q}_sec", df[f"q{q}"].apply(_cvt2seconds))
    
    return df


def qualify_result() -> None:
    """Display qualifying result view."""
    # read data
    df = _read_data()

    # header
    st.header("Qualify result")

    # select season to visualize
    list_season = np.sort(df["year"].unique())[::-1].tolist()
    selected_season = st.selectbox("Select season", list_season, key="selected_season_qualify_result")
    df_season = df[df["year"] == selected_season]

    # select round(grand prix) to visualize
    df_season.insert(
        0, "round_str",
        [str(x) if x >= 10 else "0" + str(x) for x in df_season["round"]])
    df_season.insert(
        0, "round(gp)", df_season["round_str"] + " (" +
        df_season["name"].str.replace(" Grand Prix", "") + ")")
    list_round = np.sort(df_season["round(gp)"].unique()).tolist()
    selected_round = st.selectbox("Select round", list_round, key="selected_round_qualify_result")
    df_season_round = df_season[df_season["round(gp)"] == selected_round]

    # qualifying time of selected grand prix
    df_qualify = pd.DataFrame({"driver":df_season_round["driverRef"].tolist()*3,
                      "qualifying time(sec)":df_season_round["q1_sec"].tolist() + \
                      df_season_round["q2_sec"].tolist() + \
                      df_season_round["q3_sec"].tolist(),
                      "qualifying round":(
                          ["q1"]*len(df_season_round)) + \
                          (["q2"]*len(df_season_round))+ \
                          (["q3"]*len(df_season_round)
                       ),
                      "position": df_season_round["position"].tolist()*3
                      })
    df_qualify = df_qualify.sort_values(by=["position", "qualifying round"]).reset_index(drop=True)
    df_qualify.insert(
        len(df_qualify.columns), 
        "gap to fastest time(%)", 
        (
            (
                (df_qualify["qualifying time(sec)"] - df_qualify["qualifying time(sec)"].min()) / \
                df_qualify["qualifying time(sec)"].min()
            )*100
        ).round(3)
    )

    # select index to visualize
    selected_item = "qualifying time(sec)"
    if st.checkbox("Gap (%)", key="check_gap_qualify_result"):
        selected_item = "gap to fastest time(%)"

    # visualize by plotly
    fig = px.scatter(df_qualify, x="driver", y=selected_item, color="qualifying round")
    fig.update_traces(marker_size=10)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    qualify_result()
