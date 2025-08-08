"""Leakage guard checks to enforce no future data is used."""

from __future__ import annotations
import sqlite3


def assert_no_post_asof_rows(processed_db: str, season: int, asof: str) -> None:
    """Ensure that there are no rows dated after the as-of date.  Placeholder."""
    # In a full implementation, query the games and metrics tables to ensure no data
    # after `asof` is present for the given season.
    return None


def assert_feature_dates_valid(processed_db: str, season: int, asof: str) -> None:
    """Ensure that feature as-of dates are valid.  Placeholder implementation."""
    # TODO: verify that team_metrics.asof_date <= asof
    return None
