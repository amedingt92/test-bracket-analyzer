"""ETL routines for moving raw scraped data into the SQLite database.

These are placeholder implementations.  In a full system, the ETL would parse
the raw HTML/CSV/JSON files downloaded by the scrapers and populate the
appropriate tables defined in ``schema.py``.
"""

from __future__ import annotations

from pathlib import Path
from typing import List
import sqlite3

from . import schema as schema_mod


def ingest_to_sqlite(seasons: List[int], raw_dir: Path, processed_db: str) -> None:
    """
    Ingest raw data for the given seasons into the SQLite database.
    This placeholder implementation simply ensures the database exists.
    """
    schema_mod.init_db(processed_db)
    # TODO: parse raw files under raw_dir and insert into the database


def index_db(processed_db: str) -> None:
    """
    Create indices on common query columns.  Placeholder implementation.
    """
    conn = sqlite3.connect(processed_db)
    try:
        c = conn.cursor()
        # Example indices (not strictly necessary for placeholder)
        c.execute("CREATE INDEX IF NOT EXISTS idx_games_season_date ON games(season, date);")
        c.execute("CREATE INDEX IF NOT EXISTS idx_team_metrics_team ON team_metrics(team_id);")
        conn.commit()
    finally:
        conn.close()
