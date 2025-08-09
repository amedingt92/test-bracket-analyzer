"""
Mock scraper for Bart Torvik data.

This placeholder implementation demonstrates how a data scraper might
download and save raw game and team data for the specified seasons.
Because network access is not available in this environment and the real
Torvik site’s structure may change, this function simply writes a small
synthetic dataset to the `raw_dir` for each season.

When implementing a real scraper, you would:
  * Use `requests` or `aiohttp` to fetch HTML/CSV files from the Torvik
    website.
  * Parse the content with `pandas.read_csv` or BeautifulSoup.
  * Respect the site’s robots.txt and terms of service.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import List, Dict, Any


def scrape_torvik(seasons: List[int], raw_dir: Path, config: Dict[str, Any]) -> None:
    """
    Generate dummy game and team CSV files for each season.

    Parameters
    ----------
    seasons : List[int]
        The seasons to scrape.
    raw_dir : Path
        Directory where raw CSV files will be saved.
    config : Dict[str, Any]
        Configuration dictionary; unused in this mock implementation but
        included to mirror the signature of a real scraper.
    """
    raw_dir.mkdir(parents=True, exist_ok=True)
    for season in seasons:
        games_path = raw_dir / f"{season}_games.csv"
        teams_path = raw_dir / f"{season}_teams.csv"
        # Generate a simple round‑robin schedule between four teams
        teams = [f"T{idx}" for idx in range(1, 5)]
        # Write teams CSV
        with teams_path.open("w", newline="", encoding="utf-8") as tf:
            writer = csv.writer(tf)
            writer.writerow(["team_id", "name"])
            for t in teams:
                writer.writerow([t, f"Team {t}"])
        # Write games CSV
        with games_path.open("w", newline="", encoding="utf-8") as gf:
            writer = csv.writer(gf)
            writer.writerow(["date", "home_team_id", "away_team_id", "home_score", "away_score", "neutral"])
            for home in teams:
                for away in teams:
                    if home == away:
                        continue
                    # Assign a date in January
                    date = f"{season}-01-{random.randint(1, 28):02d}"
                    home_score = random.randint(60, 90)
                    away_score = random.randint(60, 90)
                    neutral = 0
                    writer.writerow([date, home, away, home_score, away_score, neutral])
