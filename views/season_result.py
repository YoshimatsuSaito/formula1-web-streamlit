import os

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

current_dir = os.path.dirname(__file__)


def read_data() -> pd.DataFrame:
    """Read data."""
    df_driver_standings = pd.read_csv(
        os.path.join(current_dir, "../data/driver_standings.csv")
    )
    df_drivers = pd.read_csv(os.path.join(current_dir, "../data/drivers.csv"))
    df_races = pd.read_csv(os.path.join(current_dir, "../data/races.csv"))
    df = pd.merge(df_driver_standings, df_drivers, on=["driverId"], how="left")
    df = pd.merge(df, df_races, on=["raceId"], how="left")
    return df


def season_result() -> None:
    """Display season result view."""
    df = read_data()

    # header
    st.header("Season result")

    # select season to visualize
    list_season = np.sort(df["year"].unique())[::-1].tolist()
    selected_season = st.selectbox(
        "Select season", list_season, key="selected_season_season_result"
    )
    df_season = df[df["year"] == selected_season]

    # select drivers to visualize
    list_drivers = (
        df_season.groupby("driverRef")["points"]
        .max()
        .sort_values(ascending=False)
        .index.tolist()
    )
    list_default_drivers = list_drivers[:5]
    selected_items = st.multiselect(
        "Select drivers (default = top 5 of the season)",
        options=list_drivers,
        default=list_default_drivers,
        key="selected_drivers_season_result",
    )
    if st.checkbox("All drivers ", key="check_alldrivers_season_result"):
        selected_items = list_drivers
    df_season_drivers = df_season[df_season["driverRef"].isin(selected_items)]
    df_season_drivers = (
        df_season_drivers.loc[:, ["round", "points", "driverRef", "name"]]
        .sort_values(by="round")
        .reset_index(drop=True)
    )
    df_season_drivers["name"] = df_season_drivers["name"].str.replace(" Grand Prix", "")

    # visualize by plotly
    list_order_points = (
        df_season_drivers.groupby("driverRef")["points"]
        .max()
        .sort_values(ascending=False)
        .index.tolist()
    )
    fig = px.line(
        df_season_drivers,
        x="round",
        y="points",
        color="driverRef",
        labels={"driverRef": "driver", "name": "Grand Prix"},
        category_orders={"driverRef": list_order_points},
    )
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tick0=1,
            dtick=1,
            tickvals=df_season_drivers["round"].tolist(),
            ticktext=df_season_drivers["name"].tolist(),
        )
    )
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    season_result()
