"""Data standardization routines."""

import sqlite3
from typing import Optional


def standardize_team_names(processed_db: str) -> None:
    """
    Standardize team names across sources using a simple normalization.
    This placeholder implementation does not modify the database but would
    ideally update the `teams` table with normalized names and canonical IDs.
    """
    # TODO: implement rapidfuzz-based name matching across sources
    return None


def compute_experience_proxy(processed_db: str) -> None:
    """
    Compute an experience proxy for each team and store it in the database.
    Placeholder implementation.
    """
    # TODO: derive experience from roster or age; use players table if available
    return None
