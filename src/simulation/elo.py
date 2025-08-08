"""Simple Elo rating model implementation."""

import pandas as pd
from typing import Dict


def train_elo(games_df: pd.DataFrame, config: dict) -> dict:
    """
    Train Elo ratings based on historical games.

    Parameters
    ----------
    games_df : DataFrame
        Columns must include home_team_id, away_team_id, home_score, away_score, neutral.
    config : dict
        Configuration with keys k_base, home_adv, preseason_regress.

    Returns
    -------
    dict
        Mapping of team_id to final Elo rating.
    """
    k_base = config.get("k_base", 30)
    home_adv = config.get("home_adv", 40)
    ratings: Dict[str, float] = {}
    # Initialize teams with 1500
    for team in pd.concat([games_df["home_team_id"], games_df["away_team_id"]]).unique():
        ratings[team] = 1500.0
    # Process games chronologically
    for _, row in games_df.iterrows():
        home = row["home_team_id"]
        away = row["away_team_id"]
        home_score = row["home_score"]
        away_score = row["away_score"]
        neutral = row.get("neutral", 0)
        # Compute expected outcome
        elo_home = ratings.get(home, 1500.0)
        elo_away = ratings.get(away, 1500.0)
        diff = elo_home - elo_away + (0 if neutral else home_adv)
        expected_home = 1 / (1 + 10 ** (-diff / 400))
        # Actual outcome: 1 if home wins, 0 otherwise
        actual_home = 1.0 if home_score > away_score else 0.0
        delta = k_base * (actual_home - expected_home)
        ratings[home] = elo_home + delta
        ratings[away] = elo_away - delta
    return ratings


def predict_elo_prob(model: dict, team_a: str, team_b: str, neutral: bool) -> float:
    """
    Predict probability that team_a beats team_b using Elo ratings.

    Parameters
    ----------
    model : dict
        Mapping of team_id to Elo rating.
    team_a : str
        Team A id.
    team_b : str
        Team B id.
    neutral : bool
        Whether the game is on a neutral court.

    Returns
    -------
    float
        Probability of team A winning.
    """
    elo_a = model.get(team_a, 1500.0)
    elo_b = model.get(team_b, 1500.0)
    diff = elo_a - elo_b
    # Home advantage is not applied here because the caller should set neutral accordingly.
    prob_a = 1 / (1 + 10 ** (-diff / 400))
    return float(prob_a)
