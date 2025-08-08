"""Simple Bayesian update model."""

from typing import Dict


def bayes_prior(team_id: str, features_row: dict, config: dict) -> float:
    """
    Return an initial prior win probability for a team based on features.

    Placeholder implementation returns 0.5 for all teams.
    """
    return 0.5


def bayes_update(prior: float, game_result: int, strength: float) -> float:
    """
    Update a prior probability given a binary game result (1 win, 0 loss).
    The strength controls how much influence the new data has.

    posterior = (prior * strength + game_result) / (strength + 1)
    """
    return (prior * strength + game_result) / (strength + 1)
