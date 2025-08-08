"""Feature utilities for simulations."""

import pandas as pd


def head_to_head_features(features_df: pd.DataFrame, team_a: str, team_b: str) -> pd.Series:
    """
    Generate a Series of head-to-head feature differences between team_a and team_b.

    Placeholder implementation: returns the difference in adj_o and adj_d if
    present, otherwise zeros.
    """
    row_a = features_df.loc[features_df["team_id"] == team_a]
    row_b = features_df.loc[features_df["team_id"] == team_b]
    if row_a.empty or row_b.empty:
        return pd.Series({"adj_o_diff": 0.0, "adj_d_diff": 0.0})
    diff = row_a.iloc[0] - row_b.iloc[0]
    return pd.Series({"adj_o_diff": diff.get("adj_o", 0.0), "adj_d_diff": diff.get("adj_d", 0.0)})


def style_contrast(features_df: pd.DataFrame, team_a: str, team_b: str) -> float:
    """
    Compute a scalar measure of style contrast between two teams.

    Placeholder implementation: returns zero.
    """
    return 0.0
