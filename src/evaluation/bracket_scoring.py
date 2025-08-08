"""Functions for scoring tournament brackets."""

from typing import Dict


def score_bracket(picks: Dict[str, str], truth: Dict[str, str], system: str, config: dict) -> int:
    """
    Compute a bracket score.

    Parameters
    ----------
    picks : dict
        Mapping of game_id to predicted winner_id.
    truth : dict
        Mapping of game_id to actual winner_id.
    system : str
        Scoring system name ('espn', 'yahoo', 'custom').
    config : dict
        Scoring configuration loaded from scoring.yaml.

    Returns
    -------
    int
        Total points scored.
    """
    # Placeholder scoring: 1 point per correct pick
    score = 0
    for game_id, winner in picks.items():
        if truth.get(game_id) == winner:
            score += 1
    return score
