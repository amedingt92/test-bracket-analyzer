"""SQLite schema definitions for March Madness data."""

import sqlite3


def init_db(db_path: str) -> None:
    """Initialize the SQLite database with all required tables."""
    conn = sqlite3.connect(db_path)
    try:
        c = conn.cursor()
        # Enable foreign keys
        c.execute("PRAGMA foreign_keys = ON;")
        # Create tables
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS teams(
              team_id TEXT PRIMARY KEY,
              name TEXT,
              conference TEXT,
              season INTEGER,
              division TEXT,
              source TEXT,
              created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS games(
              game_id TEXT PRIMARY KEY,
              season INTEGER,
              date TEXT,
              home_team_id TEXT,
              away_team_id TEXT,
              home_score INTEGER,
              away_score INTEGER,
              venue_id TEXT,
              neutral INTEGER,
              source TEXT
            );

            CREATE TABLE IF NOT EXISTS tournament_games(
              game_id TEXT PRIMARY KEY,
              season INTEGER,
              round INTEGER,
              region TEXT,
              date TEXT,
              team_a_id TEXT,
              team_b_id TEXT,
              team_a_seed INTEGER,
              team_b_seed INTEGER,
              winner_id TEXT,
              site TEXT,
              source TEXT
            );

            CREATE TABLE IF NOT EXISTS seeds(
              season INTEGER,
              team_id TEXT,
              seed INTEGER,
              region TEXT,
              PRIMARY KEY (season, team_id)
            );

            CREATE TABLE IF NOT EXISTS team_metrics(
              team_id TEXT,
              season INTEGER,
              asof_date TEXT,
              adj_o REAL, adj_d REAL, tempo REAL, sos REAL, luck REAL, exp REAL,
              source TEXT,
              PRIMARY KEY (team_id, season, asof_date, source)
            );

            CREATE TABLE IF NOT EXISTS players(
              player_id TEXT,
              team_id TEXT,
              season INTEGER,
              name TEXT,
              pos TEXT,
              height TEXT,
              PRIMARY KEY (player_id, season)
            );

            CREATE TABLE IF NOT EXISTS injuries_free_text(
              season INTEGER,
              team_id TEXT,
              date TEXT,
              note TEXT,
              PRIMARY KEY (season, team_id, date)
            );

            CREATE TABLE IF NOT EXISTS venues(
              venue_id TEXT PRIMARY KEY,
              name TEXT,
              city TEXT, state TEXT, lat REAL, lon REAL
            );
            """
        )
        conn.commit()
    finally:
        conn.close()
