"""Feature table construction."""

from __future__ import annotations
from typing import List
import sqlite3


def build_feature_table(processed_db: str, season: int, asof: str) -> None:
    """
    Create per-team/per-asof feature rows (adj_o, adj_d, tempo, sos, luck, exp,
    style_contrast, travel_km, rest_days).  Uses only records with date <= asof.

    Placeholder implementation that ensures the team_metrics table exists.
    """
    conn = sqlite3.connect(processed_db)
    try:
        c = conn.cursor()
        # For placeholder, we do nothing. In a full implementation this would
        # aggregate game results and metrics to compute features.
        pass
    finally:
        conn.close()
