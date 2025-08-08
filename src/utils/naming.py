"""Utilities for canonicalizing team names."""

import re


def normalize_team_name(name: str) -> str:
    """
    Normalize a team name by lowering case, removing punctuation and extra spaces.

    This is a simplified normalizer.  In practice you may need to use more
    sophisticated fuzzy matching (see rapidfuzz) to match across sources.
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9 ]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def team_key(name: str, season: int) -> str:
    """Create a unique key for a team given its name and season."""
    return f"{normalize_team_name(name)}_{season}"
