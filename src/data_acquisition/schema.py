"""
Database schema definitions for the March Madness prediction system.

This module contains functions to initialize the SQLite database used by the
pipeline.  It creates tables for games and teams along with simple indices.
In a full implementation you would extend this schema to include additional
tables (e.g. tournament brackets, seeds, injuries, venues) and enforce
foreign‑key relationships.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def init_db(db_path: str) -> None:
    """Create the SQLite database schema if it does not already exist.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.  If the file does not exist it will
        be created; if it does exist the function will ensure required tables
        are present.
    """
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        # Create a simple games table.  In practice you would include more
        # fields such as location, neutral flag, tournament round, etc.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season INTEGER NOT NULL,
                date TEXT NOT NULL,
                home_team_id TEXT NOT NULL,
                away_team_id TEXT NOT NULL,
                home_score INTEGER NOT NULL,
                away_score INTEGER NOT NULL,
                neutral INTEGER DEFAULT 0
            );
            """
        )
        # Create a teams table with basic metadata.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_id TEXT NOT NULL,
                season  INTEGER NOT NULL,
                name    TEXT NOT NULL,
                PRIMARY KEY (team_id, season)
            );
            """
        )
        # Create basic indices to speed common queries.
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_games_season_date ON games(season, date);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_games_home_team ON games(home_team_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_games_away_team ON games(away_team_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_teams_season ON teams(season);"
        )
        conn.commit()
    finally:
        conn.close()
