"""
Feature utilities for pairwise matchups.  These functions operate on
prepared feature tables and compute additional comparison features such as
style contrast.  They are used by the logistic regression and ensemble
models.
"""

from __future__ import annotations

import pandas as pd

def head_to_head_features(features_df: pd.DataFrame, team_a: str, team_b: str) -> pd.Series:
    """Construct a feature vector for a match‑up between two teams.

    The function handles both indexed DataFrames (where the index is team_id)
    and DataFrames with a 'team_id' column.  Non‑numeric columns are
    ignored when computing differences.

    Args:
        features_df: DataFrame containing per‑team features.
        team_a: Team ID for the first team.
        team_b: Team ID for the second team.
    Returns:
        A Series representing the difference in features (team A minus team B).
    """
    # Determine how to locate the rows for the two teams
    if features_df.index.name == "team_id" or (
        features_df.index.dtype == object and team_a in features_df.index
    ):
        row_a = features_df.loc[team_a]
        row_b = features_df.loc[team_b]
    else:
        row_a = features_df.loc[features_df["team_id"] == team_a].squeeze()
        row_b = features_df.loc[features_df["team_id"] == team_b].squeeze()

    # Compute numeric columns from the DataFrame itself (not the Series)
    numeric_cols = features_df.select_dtypes(include=["number"]).columns

    # Subtract only numeric columns to avoid string subtraction
    diff = row_a[numeric_cols] - row_b[numeric_cols]

    # Rename the index to indicate differences
    diff.index = [f"{col}_diff" for col in numeric_cols]

    return diff




def style_contrast(features_df: pd.DataFrame, team_a: str, team_b: str) -> float:
    """Compute a simple style contrast metric between two teams.

    This is a placeholder implementation; real models may compare tempo,
    offensive/defensive efficiency and other qualitative factors.
    """
    # TODO: implement real style contrast metric
    diff = features_df.loc[team_a] - features_df.loc[team_b]
    return diff.abs().sum()
