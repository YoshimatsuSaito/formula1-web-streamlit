import datetime
import os
import sys

import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, "../"))

from modules.strategy_maker import create_tyre_combination, Strategy


# function to make dataframe
def get_optimization_results(pitloss, total_lap, dict_degradation, dict_pace, fuel_effect, track_improvement, dict_tyre_combi):
    list_all_result = list()
    for n_stop in dict_tyre_combi.keys():
        list_combi = dict_tyre_combi[n_stop]
        strat = Strategy(n_stop=n_stop, pitloss=pitloss, total_lap=total_lap, dict_degradation=dict_degradation, dict_pace=dict_pace, fuel_effect=fuel_effect, track_improvement=track_improvement)
        for combi in list_combi:
            res = strat.optimize(combi)
            list_res = list()

            list_stint_tyre = [x for x in combi]
            list_stint_tyre += [None] * (max(dict_tyre_combi.keys()) + 1 - len(list_stint_tyre))
            list_stint_laps = [int(x) for x in res.x]
            list_stint_laps[-1] += (total_lap - sum(list_stint_laps)) # convert float to int
            list_stint_laps += [0] * (max(dict_tyre_combi.keys()) + 1 - len(list_stint_laps))
            
            list_res += list_stint_tyre
            list_res += list_stint_laps
            list_res.append(n_stop)
            list_res.append(pitloss)
            list_res.append(total_lap)
            list_res.append(track_improvement)
            list_res.append(fuel_effect)
            list_res += list(dict_degradation.values())
            list_res += list(dict_pace.values())
            list_res.append(res.success)
            list_res.append(res.fun)

            list_all_result.append(list_res)
    df_res = pd.DataFrame(
        list_all_result, 
        columns=[
                 "tyre_1", 
                 "tyre_2", 
                 "tyre_3", 
                 "tyre_4", 
                 "laps_1", 
                 "laps_2", 
                 "laps_3", 
                 "laps_4", 
                 "n_stop", 
                 "pitloss", 
                 "total_lap", 
                 "track_improvement",
                 "fuel_effect",
                 "degradation_Soft", 
                 "degradation_Medium", 
                 "degradation_Hard", 
                 "pace_Soft", 
                 "pace_Medium", 
                 "pace_Hard", 
                 "status", 
                 "total_lap_time"
        ]
    )
    return df_res

# function to get pace at each lap
def create_list_pace(strat_data):
    list_pace = list()
    lap_in_total = 0
    track_improvement = strat_data["track_improvement"]
    fuel_effect = strat_data["fuel_effect"]
    pitloss = strat_data["pitloss"]
    n_stop = strat_data["n_stop"]
    for stint in range(1, n_stop+2):
        tyre_stint = strat_data[f"tyre_{stint}"]
        pace_stint = strat_data[f"pace_{tyre_stint}"]
        degradation_stint = strat_data[f"degradation_{tyre_stint}"]
        laps_stint = strat_data[f"laps_{stint}"]
        for lap in range(laps_stint):
            if (lap == laps_stint - 1) and (stint != n_stop+1):
                pitloss_lap = pitloss
            else:
                pitloss_lap = 0
            pace = pace_stint + (degradation_stint * lap) + pitloss_lap - (lap_in_total * (track_improvement + fuel_effect))
            list_pace.append(pace)
            lap_in_total += 1
    return list_pace

# function to visualize strategy by matplotlib
def show_pace_graph(df_res):
    plot_area = st.empty()

    total_lap = int(df_res["total_lap"].unique())
    dict_color_tyre = {"Soft": "red", "Medium": "gold", "Hard": "gray"}

    # arrange data format
    df_res_sorted = df_res.sort_values(by="total_lap_time").reset_index(drop=True)
    df_res_sorted.fillna("", inplace=True)
    df_res_sorted.insert(0, "Strategy", df_res_sorted["tyre_1"].str[:1]+df_res_sorted["tyre_2"].str[:1]+df_res_sorted["tyre_3"].str[:1]+df_res_sorted["tyre_4"].str[:1])
    df_res_sorted.index = df_res_sorted["Strategy"]
    df_res_sorted.insert(0, "diff", df_res_sorted["total_lap_time"]-df_res_sorted["total_lap_time"].min())

    fig, ax = plt.subplots(nrows=3, dpi=250, figsize=(8, 8))
    for n_idx, idx, ls in zip(range(2, -1, -1), df_res_sorted.index[:3], ["solid", "dashed", "dotted"]):
        strat_data = df_res_sorted.loc[idx]
        list_pace = create_list_pace(strat_data)
        for stint in range(1, strat_data["n_stop"]+2):
            # start position of x axis of the stint
            if stint == 1:
                start = 0
            else:
                start = 0
                for prev_stint in range(1, stint):
                    start += strat_data[f"laps_{prev_stint}"]
            # end position of x axis of the stint
            if stint == strat_data["n_stop"] + 1:
                end = strat_data["total_lap"]
            else:
                end = start + strat_data[f"laps_{stint}"] + 1 # extend line to start of next stint
            ax[1].plot(range(start, end), list_pace[start:end], color=dict_color_tyre[strat_data[f"tyre_{stint}"]], linewidth=1, linestyle=ls)
            ax[0].plot(range(start, end-1), [n_idx]*(end-start-1), color=dict_color_tyre[strat_data[f"tyre_{stint}"]], linewidth=2)
            if stint != strat_data["n_stop"] + 1:
                ax[0].text(end-1, n_idx, end-1, horizontalalignment="center", verticalalignment="bottom")
        ax[1].plot([0], [list_pace[0]], color="k", linestyle=ls, label=idx)

    # strategy graph
    ax[0].set_title("Best three strategies")
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['left'].set_visible(False)
    ax[0].set_xlabel("Lap")
    ax[0].set_ylabel("Strategy")
    ax[0].set_yticks(range(3))
    ax[0].set_yticklabels(["Third\nfastest", "Second\nfastest", "Fastest"])
    ax[0].set_ylim(-0.5, 3)
    ax[0].set_xticks([0] + list(range(9, total_lap-1+10, 10)))
    ax[0].set_xticklabels([1] + list(range(10, total_lap+10, 10)))
    ax[0].set_xlim(0, total_lap-1)
    for k, v in dict_color_tyre.items():
        ax[0].plot([0], [0], color=v, linestyle="solid", label=k)
    ax[0].legend(loc="best", ncol=3)

    # pace graph
    ax[1].set_title("Pace graph of fastest strategies")
    ax[1].set_xlabel("Lap")
    ax[1].set_ylabel("Pace(sec)")
    ax[1].legend(loc="upper center", ncol=3)
    ax[1].set_xticks([0] + list(range(9, total_lap-1+10, 10)))
    ax[1].set_xticklabels([1] + list(range(10, total_lap+10, 10)))
    ax[1].set_xlim(0, total_lap-1)
    ax[1].set_ylim(min(list_pace)-3, max(list_pace)+7)

    # top 10 strategies and total time of those
    df_best10 = df_res_sorted.iloc[:10].sort_values(by="total_lap_time", ascending=False)
    df_best10["diff"].plot.barh(ax=ax[2], color="b")
    original_xticks = ax[2].get_xticks()
    added_xticklabels = [str(datetime.timedelta(seconds=int(x))) for x in original_xticks + df_best10["total_lap_time"].min()]
    ax[2].set_title("Top 10 fastest strategies")
    ax[2].set_xticks(original_xticks)
    ax[2].set_xticklabels(added_xticklabels)
    ax[2].set_xlabel("Total time")

    plt.tight_layout()
    
    plot_area.pyplot(fig)


def strategy():
    st.header("Optimal strategy")
    st.subheader("Input information")
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        total_lap = st.number_input(
            label="Total race laps", 
            value=60, 
            min_value=0, 
            max_value=100, 
            step=1
        )
    with col_2:
        pitloss = st.number_input(
            label="Pitloss(sec)", 
            value=25.0, 
            min_value=0.0, 
            max_value=100.0, 
            step=0.1, 
            format="%.1f"
        )
    with col_3:
        track_improvement = st.number_input(
            label="Track improvement(sec)", 
            value=0.005, 
            min_value=0.0, 
            max_value=1.0, 
            step=0.001, 
            format="%.3f"
        )
    with col_4:
        fuel_effect = st.number_input(
            label="Fuel effect(sec)",
            value=0.005, 
            min_value=0.0, 
            max_value=1.0, 
            step=0.001, 
            format="%.3f"
        )
    
    col_soft, col_medium, col_hard = st.columns(3)
    dict_degradation = dict()
    dict_pace = dict()
    
    for col, tyre_name, default_degradation, default_pace in zip(
        [col_soft, col_medium, col_hard], 
        ["Soft", "Medium", "Hard"], 
        [0.2, 0.08, 0.03], 
        [79.0, 80.0, 81.0]
    ):
        with col:
            st.subheader(tyre_name)
            dict_degradation[tyre_name] = st.number_input(
                label=f"Degradation(sec/lap)", 
                value=default_degradation, 
                key=tyre_name, 
                min_value=0.0, 
                max_value=100.0, 
                step=0.01,
                format="%.2f"
            )
            dict_pace[tyre_name] = st.number_input(
                label=f"Pace(sec/lap)", 
                value=default_pace, 
                key=tyre_name, 
                min_value=0.0, 
                max_value=100.0, 
                step=0.01,
                format="%.2f"
            )
    
    # get combination of tyre
    dict_tyre_combi = create_tyre_combination()
    
    # start calculate optimal strategy when this button is pushed
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        button_ = st.button("Calculate optimal strategy!")
    if button_:
        # get optimal strategy based on given tyre combination
        df_res = get_optimization_results(
            pitloss=pitloss,
            total_lap=total_lap,
            dict_degradation=dict_degradation,
            dict_pace=dict_pace,
            track_improvement=track_improvement,
            fuel_effect=fuel_effect,
            dict_tyre_combi=dict_tyre_combi
        )
        
        # visualize optimal strategies
        st.subheader("Optimal strategies based on given information above")
        show_pace_graph(df_res=df_res)
    


if __name__ == "__main__":
    strategy()