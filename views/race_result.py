import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

current_dir = os.path.dirname(__file__)


def race_result():
    # read data
    df_results = pd.read_csv(os.path.join(current_dir, "../data/results.csv"))
    df_drivers = pd.read_csv(os.path.join(current_dir, "../data/drivers.csv"))
    df_races = pd.read_csv(os.path.join(current_dir, "../data/races.csv"))
    df = pd.merge(df_results, df_drivers, on=["driverId"], how="left")
    df = pd.merge(df, df_races, on=["raceId"], how="left")

    # header
    st.header("Race result")

    # select season to visualize
    list_season = np.sort(df["year"].unique())[::-1].tolist()
    if 2022 in list_season:
        list_season.remove(2022)
    selected_season = st.selectbox("Select season", list_season)
    df_season = df[
        df["year"] ==
        selected_season].loc[:,
                             ["driverRef", "positionOrder", "round", "name"]]

    # to use change columns name later
    df_round_name = df_season.loc[:, ["round", "name"]].drop_duplicates()
    dict_round_name = {
        k: v
        for k, v in zip(df_round_name["round"].tolist(),
                        df_round_name["name"].tolist())
    }

    # visualize by plotly
    df_season.drop(columns=["name"], inplace=True)
    df_season = pd.pivot_table(df_season,
                               index="positionOrder",
                               columns="round",
                               aggfunc=lambda x: ' '.join(x))
    df_season.columns = [dict_round_name[x[1]] for x in df_season.columns]
    df_season.insert(0, "position", df_season.index)
    st.table(df_season)


if __name__ == "__main__":
    race_result()
