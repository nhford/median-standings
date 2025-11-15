#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from espn_api.football import League
from tqdm import tqdm
import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import re
from IPython.display import HTML

import numpy as np
from scipy.stats import gamma


season_id = 2025
league_id = "619156725"
espn_cookies = {
    "swid": "{6247CD51-062F-4B3E-87CD-51062FFB3E64}",
    "espn_s2": "AECY530cfYoQqdW0x0ELczW91RQ4%2BuWDRq93p0ieoHgEh%2FiBoTu5Ao3KjpLfGk1OihPrgjgv0TgNEVyht4LYfKqRg%2Bql271mAS9U1UxsSdTnLLCp3xX2luBKCvOlvHM2Ts7o4hw%2F99mJ4CjIUMq65UDO52NR3%2FA%2BSefhVcTjorA6Y2LHoOJRBboM3nik9hQZbH8zGbOJsWgO3jfTzO77fy9dtev781%2FmqJb192FRMAlBUG6bSZuhrj2cHdyA3dDXhfBAQCYPN0pvMD9tcOZ3gv%2Bl",
}

LEAGUE = League(
    league_id=league_id,
    year=season_id,
    espn_s2=espn_cookies["espn_s2"],
    swid=espn_cookies["swid"],
)

LINEUP_ORDERING = {
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3,
    "RB/WR/TE": 4,
}


def zeroes(lineup):
    players = [player for player in lineup if player.game_played == 0]
    return players


def rand_gamma_sum(projs, N=1000, factor=2 / 3, tamper=0.97):
    projs = np.asarray(projs, dtype=float)

    mean = projs
    std_dev = projs * factor
    shape = (mean / std_dev) ** 2
    scale = (std_dev**2) / mean

    # Draw N samples for each projection (vectorized broadcast)
    # shape: (len(projs), N)
    samples = gamma.rvs(a=shape[:, None], scale=scale[:, None], size=(len(projs), N))

    # Sum across all projections → one total per sample
    return samples.sum(axis=0) * tamper


def get_starters(lineup, ordering=LINEUP_ORDERING):
    starters = [
        player
        for player in lineup
        if (player.lineupSlot != "IR" and player.lineupSlot != "BE")
    ]
    return sorted(starters, key=lambda player: ordering[player.lineupSlot])


def get_lineups(league=LEAGUE, week=None):
    lineups = {}
    for box in league.box_scores(week=week):
        lineups[box.home_team.team_name] = {
            "score": box.home_score,
            "proj": box.home_projected,
            "lineup": box.home_lineup,
        }
        lineups[box.away_team.team_name] = {
            "score": box.away_score,
            "proj": box.away_projected,
            "lineup": box.away_lineup,
        }
    return lineups


# first mass is the total score, the remaining are player scores
def get_lineup_mass(score: float, lineup: list):
    starters = get_starters(lineup)
    # these are supposed to be the masses of players who haven't played yet
    masses = np.array(
        [
            player.projected_points - player.points
            for player in starters
            if player.game_played < 100 and player.projected_points - player.points > 0
        ]
    )
    masses = np.insert(masses, 0, score)
    return masses


def get_lineup_masses(week=None):
    lineups = get_lineups(week=week)
    for team, obj in lineups.items():
        lineups[team]["masses"] = get_lineup_mass(obj["score"], obj["lineup"])
    return lineups


def get_team_sample_scores(N=1000, week=None):
    lineups = get_lineup_masses(week)
    for team, obj in lineups.items():
        projs = rand_gamma_sum(obj["masses"][1:], N)
        projs += lineups[team]["score"]
        lineups[team]["sample_scores"] = projs
    return lineups


def column_ranks(arr, one_indexed=True, descending=True):
    sort_arr = -arr if descending else arr

    order = np.argsort(sort_arr, axis=0)
    ranks = np.empty_like(order, dtype=float)
    ranks[order, np.arange(sort_arr.shape[1])] = np.arange(sort_arr.shape[0])[:, None]

    if one_indexed:
        ranks += 1
    return ranks


# TODO: exporting median, payout as raw percent
def format_dataframe(df, payout_amount=75):
    df.columns = ["Team", "Current", "Projection", "Median", "Payout"]
    # df["Median"] = df["Median"].map(lambda x: f"{x*100:.1f}%")
    # df["Payout"] = df["Payout"].map(lambda x: f"${x * payout_amount:.2f}")
    df = df.sort_values(
        by=["Current", "Projection"], ascending=[False, False]
    ).reset_index(drop=True)
    df.index = df.index + 1
    return df


def get_median_summary(N=1000, week=None):
    sample_scores_dict = get_team_sample_scores(N, week)
    owners = sample_scores_dict.keys()
    sample_team_scores = [team["sample_scores"] for team in sample_scores_dict.values()]
    sample_scores_2d_arr = np.vstack(list(sample_team_scores))
    sample_ranks = column_ranks(sample_scores_2d_arr)
    current_scores = [team["score"] for team in sample_scores_dict.values()]
    current_projs = [team["proj"] for team in sample_scores_dict.values()]
    medians = np.sum(sample_ranks <= 6, axis=1) / N
    payouts = np.sum(sample_ranks == 1, axis=1) / N
    df = pd.DataFrame(data=[owners, current_scores, current_projs, medians, payouts]).T
    return format_dataframe(df)


get_median_summary()


# ### Gather Logos
TEAM_DICT = {}


def populate_dict(league):
    for team in league.teams:
        TEAM_DICT[team.team_name] = team.team_id


populate_dict(LEAGUE)


def getTeamID(team_name):
    return TEAM_DICT[team_name]


def make_filepath_safe(team_name: str) -> str:
    new_name = team_name.lower().replace(" ", "-")
    new_name = re.sub(r"[^a-z0-9\-_]", "", new_name)
    return new_name


def getTeamLogo(team_name, fetch=False, league=LEAGUE):
    new_team_name = make_filepath_safe(team_name)
    file_path = f"app/logos/{new_team_name}.jpg"
    if fetch or not os.path.exists(file_path):
        url = league.get_team_data(getTeamID(team_name)).logo_url
        try:
            response = requests.get(url, cookies=espn_cookies)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.convert("RGB").save(file_path, "JPEG")
        except:
            print(f"Cannot load:{file_path}")

    return file_path


def to_median_json():
    df = get_median_summary()
    df["Logo"] = df["Team"].apply(getTeamLogo)
    df = df.reset_index(drop=False, names=["Rank"])
    df.columns = list(map(lambda col: col.lower(), df.columns))
    curr_time = datetime.now().strftime("%a-%I:%M%p-%-m.%d.%y")
    df.to_json(f"backend/archive/standings-{curr_time}.json", orient="records")
    df.to_json(f"app/standings.json", orient="records")


to_median_json()
