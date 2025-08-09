"""
ETL routines for loading raw scraped data into the SQLite database.

This module defines functions that take raw data files (typically CSVs
downloaded by the scrapers) and ingest them into the project’s relational
database.  It also exposes a helper for creating indices on common query
columns.
"""

from __future__ import annotations

from pathlib import Path
from typing import List
import sqlite3
import pandas as pd

from . import schema as schema_mod


def ingest_to_sqlite(seasons: List[int], raw_dir: Path, processed_db: str) -> None:
    """
    Ingest raw CSV files for the given seasons into the SQLite database.

    Parameters
    ----------
    seasons : List[int]
        A list of season years to ingest (e.g. [2019, 2020]).
    raw_dir : Path
        Directory where raw files for each season are stored.  The expected
        naming convention is `<season>_games.csv` for game results and
        `<season>_teams.csv` for basic team metadata.  You can extend this
        function to support other file formats or more granular file naming.
    processed_db : str
        Path to the SQLite database where ingested tables will be stored.
    """
    # Ensure the database schema exists
    schema_mod.init_db(processed_db)
    conn = sqlite3.connect(processed_db)
    try:
        for season in seasons:
            # Determine file paths for the current season
            games_path = raw_dir / f"{season}_games.csv"
            teams_path = raw_dir / f"{season}_teams.csv"
            if games_path.exists():
                # Load games CSV into a DataFrame.  Expect columns:
                # date (YYYY‑MM‑DD), home_team_id, away_team_id, home_score,
                # away_score and optional neutral flag (1/0).  Additional
                # columns will be ignored.
                games_df = pd.read_csv(games_path)
                # Cast data types explicitly to avoid SQLite type confusion
                games_df = games_df.assign(
                    season=season,
                    date=games_df["date"].astype(str),
                    home_team_id=games_df["home_team_id"].astype(str),
                    away_team_id=games_df["away_team_id"].astype(str),
                    home_score=games_df["home_score"].astype(int),
                    away_score=games_df["away_score"].astype(int),
                    neutral=games_df.get("neutral", 0).fillna(0).astype(int),
                )[
                    [
                        "season",
                        "date",
                        "home_team_id",
                        "away_team_id",
                        "home_score",
                        "away_score",
                        "neutral",
                    ]
                ]
                games_df.to_sql("games", conn, if_exists="append", index=False)
            else:
                raise FileNotFoundError(f"Missing games CSV: {games_path}")

            if teams_path.exists():
                teams_df = pd.read_csv(teams_path)
                # Expect columns team_id and name; ignore others
                teams_df = teams_df.assign(
                    season=season,
                    team_id=teams_df["team_id"].astype(str),
                    name=teams_df["name"].astype(str),
                )[["team_id", "season", "name"]]
                teams_df.to_sql("teams", conn, if_exists="append", index=False)
            else:
                raise FileNotFoundError(f"Missing teams CSV: {teams_path}")
        conn.commit()
    finally:
        conn.close()


def index_db(processed_db: str) -> None:
    """
    Create indices on common query columns in the SQLite database.

    Although indices are created when the schema is initialised, this helper
    re‑creates them explicitly.  Calling this after ingestion ensures that
    indices reflect the latest data state.
    """
    conn = sqlite3.connect(processed_db)
    try:
        c = conn.cursor()
        # Recreate indices (no‑ops if already present)
        c.execute("CREATE INDEX IF NOT EXISTS idx_games_season_date ON games(season, date);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_games_home_team ON games(home_team_id);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_games_away_team ON games(away_team_id);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_teams_season ON teams(season);")
        conn.commit()
    finally:
        conn.close()
