#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from espn_api.football import League
from PIL import Image
from scipy.stats import gamma

load_dotenv()

season_id = int(os.environ.get("ESPN_SEASON_ID") or "2025")
league_id = os.environ.get("ESPN_LEAGUE_ID") or "619156725"
espn_s2 = os.environ.get("ESPN_S2")
swid = os.environ.get("ESPN_SWID")

if not espn_s2 or not swid:
    raise SystemExit(
        "Missing ESPN_S2 and/or ESPN_SWID. "
        "Copy .env.example to .env (local) or set GitHub Actions secrets."
    )

espn_cookies = {"swid": swid, "espn_s2": espn_s2}

LEAGUE = League(
    league_id=league_id,
    year=season_id,
    espn_s2=espn_cookies["espn_s2"],
    swid=espn_cookies["swid"],
)

MEDIAN_CUTOFF = len(LEAGUE.teams) // 2
SIM_N = int(os.environ.get("SIM_N") or "1000")

LINEUP_ORDERING = {
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3,
    "RB/WR/TE": 4,
}


def rand_gamma_sum(projs, N=1000, factor=2 / 3, tamper=0.97):
    projs = np.asarray(projs, dtype=float)
    if len(projs) == 0:
        return np.zeros(N)

    mean = projs
    std_dev = projs * factor
    shape = (mean / std_dev) ** 2
    scale = (std_dev**2) / mean

    # Draw N samples for each projection (vectorized broadcast)
    samples = gamma.rvs(a=shape[:, None], scale=scale[:, None], size=(len(projs), N))

    # Sum across all projections → one total per sample
    return samples.sum(axis=0) * tamper


def get_starters(lineup, ordering=LINEUP_ORDERING):
    starters = [
        player
        for player in lineup
        if player.lineupSlot != "IR" and player.lineupSlot != "BE"
    ]
    return sorted(
        starters, key=lambda player: ordering.get(player.lineupSlot, 99)
    )


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


def get_lineup_mass(score: float, lineup: list):
    starters = get_starters(lineup)
    # Masses for players who haven't finished playing yet
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


def format_dataframe(df):
    df.columns = ["Team", "Current", "Projection", "Median", "Payout"]
    df = df.sort_values(
        by=["Current", "Projection"], ascending=[False, False]
    ).reset_index(drop=True)
    df.index = df.index + 1
    return df


def get_median_summary(N=SIM_N, week=None, median_cutoff=MEDIAN_CUTOFF):
    sample_scores_dict = get_team_sample_scores(N, week)
    owners = sample_scores_dict.keys()
    sample_team_scores = [team["sample_scores"] for team in sample_scores_dict.values()]
    sample_scores_2d_arr = np.vstack(list(sample_team_scores))
    sample_ranks = column_ranks(sample_scores_2d_arr)
    current_scores = [team["score"] for team in sample_scores_dict.values()]
    current_projs = [team["proj"] for team in sample_scores_dict.values()]
    medians = np.sum(sample_ranks <= median_cutoff, axis=1) / N
    payouts = np.sum(sample_ranks == 1, axis=1) / N
    df = pd.DataFrame(data=[owners, current_scores, current_projs, medians, payouts]).T
    return format_dataframe(df)


TEAM_DICT = {}


def populate_dict(league):
    for team in league.teams:
        TEAM_DICT[team.team_name] = team.team_id


populate_dict(LEAGUE)


def getTeamID(team_name):
    return TEAM_DICT[team_name]


def make_filepath_safe(team_name: str) -> str:
    new_name = team_name.lower().strip().replace(" ", "-")
    new_name = re.sub(r"[^a-z0-9\-_]", "", new_name)
    return new_name


def getTeamLogo(team_name, fetch=False, league=LEAGUE):
    new_team_name = make_filepath_safe(team_name)
    os.makedirs("app/logos", exist_ok=True)
    file_path = f"app/logos/{new_team_name}.jpg"
    if fetch or not os.path.exists(file_path):
        url = league.get_team_data(getTeamID(team_name)).logo_url
        try:
            response = requests.get(url, cookies=espn_cookies, timeout=20)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img.convert("RGB").save(file_path, "JPEG")
        except Exception as exc:
            print(f"Cannot load {file_path}: {exc}")

    return file_path


def save_metadata(display_time):
    current_week = LEAGUE.current_week
    metadata = {"last_updated": display_time, "current_week": current_week}
    with open("app/metadata.json", "w") as json_file:
        json.dump(metadata, json_file, indent=4)


def to_median_json():
    df = get_median_summary()
    df["Logo"] = df["Team"].apply(getTeamLogo)
    df = df.reset_index(drop=False, names=["Rank"])
    df.columns = [col.lower() for col in df.columns]
    curr_time = datetime.now()
    file_time = curr_time.strftime("%a-%I:%M%p-%-m.%d.%y")
    display_time = (
        curr_time.strftime("%A, %b %-d %-I:%M%p")
        .replace("PM", "pm")
        .replace("AM", "am")
    )
    save_metadata(display_time)
    os.makedirs("backend/archive", exist_ok=True)
    df.to_json(f"backend/archive/standings-{file_time}.json", orient="records")
    df.to_json("app/standings.json", orient="records")


if __name__ == "__main__":
    to_median_json()
