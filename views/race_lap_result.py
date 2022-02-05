import os

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

current_dir = os.path.dirname(__file__)


# convert lap time written by string to seconds
def cvt2seconds(t):
    list_tmp = [
        float(x) if i == 1 else float(x) * 60
        for i, x in enumerate(t.split(":"))
    ]
    sec = list_tmp[0] + list_tmp[1]
    return sec


# pad laps
def padding(driver, total_lap, df_season_round_grpd):
    list_tmp = df_season_round_grpd.get_group(driver).tolist()
    n_short = total_lap - len(list_tmp)
    list_tmp += [np.nan] * n_short
    return list_tmp


def race_lap_result():
    # read data
    df_laptimes = pd.read_csv(
        os.path.join(current_dir, "../data/lap_times.csv"),
        usecols=["driverId", "position", "time", "raceId", "lap"])
    df_drivers = pd.read_csv(os.path.join(current_dir, "../data/drivers.csv"),
                             usecols=["driverId", "driverRef"])
    df_races = pd.read_csv(os.path.join(current_dir, "../data/races.csv"),
                           usecols=["raceId", "name", "round", "year"])
    df_results = pd.read_csv(os.path.join(current_dir, "../data/results.csv"),
                             usecols=["raceId", "driverId", "positionOrder"])
    df = pd.merge(df_laptimes, df_drivers, on=["driverId"], how="left")
    df = pd.merge(df, df_races, on=["raceId"], how="left")
    df = pd.merge(df, df_results, on=["raceId", "driverId"], how="left")
    df.insert(len(df.columns), "time_sec", df["time"].apply(cvt2seconds))

    # header
    st.header("Race result")

    # select season to visualize
    list_season = np.sort(df["year"].unique())[::-1].tolist()
    if 2022 in list_season:
        list_season.remove(2022)
    selected_season = st.selectbox("Select season", list_season)
    df_season = df[df["year"] == selected_season]

    # select round(grand prix) to visualize
    df_season.insert(
        0, "round_str",
        [str(x) if x >= 10 else "0" + str(x) for x in df_season["round"]])
    df_season.insert(
        0, "round(gp)", df_season["round_str"] + " (" +
        df_season["name"].str.replace(" Grand Prix", "") + ")")
    list_round = np.sort(df_season["round(gp)"].unique()).tolist()
    selected_round = st.selectbox("Select round", list_round)
    df_season_round = df_season[df_season["round(gp)"] == selected_round]

    # select drivers to visualize
    list_drivers = df_season_round.groupby(
        "driverRef")["positionOrder"].unique().sort_values(
            ascending=True).index.tolist()
    list_default_drivers = list_drivers[:5]
    selected_items = st.multiselect("Select drivers (default = top 5 drivers)",
                                    options=list_drivers,
                                    default=list_default_drivers)
    if st.checkbox("All drivers"):
        selected_items = list_drivers

    # make variables
    total_lap = df_season_round["lap"].max()
    winner = list_drivers[0]

    # sort by laps and groupby driver
    df_season_round_grpd = df_season_round.sort_values(
        by="lap").groupby("driverRef")["time_sec"]

    # total lap time of eventual winner at each lap
    array_winner_cumsum_lap = np.cumsum(
        padding(winner, total_lap, df_season_round_grpd))
    list_laptime = list()
    list_gap = list()
    list_driver = list()
    list_lap = list()
    for driver in df_season_round["driverRef"].unique():
        list_tmp = padding(driver, total_lap, df_season_round_grpd)
        list_laptime += list_tmp
        list_gap += list(np.cumsum(list_tmp) - array_winner_cumsum_lap)
        list_driver += [driver] * total_lap
        list_lap += list(range(1, total_lap + 1))
    df_lap = pd.DataFrame({
        "time(sec)": list_laptime,
        "driver": list_driver,
        "lap": list_lap,
        "gap to winner(sec)": list_gap
    })
    df_lap = df_lap[df_lap["driver"].isin(selected_items)]
    df_lap = pd.merge(
        df_lap,
        df_season_round.loc[:,
                            ["driverRef", "positionOrder"]].drop_duplicates(),
        left_on=["driver"],
        right_on=["driverRef"],
        how="left")
    df_lap = df_lap.sort_values(by=["lap", "positionOrder"]).reset_index(
        drop=True)

    # visualize by plotly
    # lap time at each lap
    fig = px.line(df_lap, x="lap", y="time(sec)", color="driver")
    fig.update_layout(xaxis=dict(
        tickmode='linear', tick0=1.0, dtick=5.0, tickfont=dict(size=10)))
    fig.update_xaxes(tickangle=0)
    st.plotly_chart(fig)

    # total lap time gap to eventual winner at each lap
    fig = px.line(df_lap, x="lap", y="gap to winner(sec)", color="driver")
    fig.update_layout(xaxis=dict(
        tickmode='linear', tick0=1.0, dtick=5.0, tickfont=dict(size=10)))
    st.plotly_chart(fig)


if __name__ == "__main__":
    race_lap_result()
