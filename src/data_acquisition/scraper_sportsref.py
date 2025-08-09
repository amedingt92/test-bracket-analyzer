"""
Mock scraper for Sports‑Reference data.

This placeholder writes synthetic game and team data to CSV files for
testing purposes.  Replace this implementation with real scraping logic
that fetches data from Sports‑Reference and saves it in the expected format.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import List, Dict, Any


def scrape_sportsref(seasons: List[int], raw_dir: Path, config: Dict[str, Any]) -> None:
    """Generate dummy data for Sports‑Reference."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    for season in seasons:
        games_path = raw_dir / f"{season}_games.csv"
        teams_path = raw_dir / f"{season}_teams.csv"
        teams = [f"SR{idx}" for idx in range(1, 5)]
        with teams_path.open("w", newline="", encoding="utf-8") as tf:
            writer = csv.writer(tf)
            writer.writerow(["team_id", "name"])
            for t in teams:
                writer.writerow([t, f"SportsRef {t}"])
        with games_path.open("w", newline="", encoding="utf-8") as gf:
            writer = csv.writer(gf)
            writer.writerow(["date", "home_team_id", "away_team_id", "home_score", "away_score", "neutral"])
            for home in teams:
                for away in teams:
                    if home == away:
                        continue
                    date = f"{season}-02-{random.randint(1, 28):02d}"
                    home_score = random.randint(60, 90)
                    away_score = random.randint(60, 90)
                    neutral = 0
                    writer.writerow([date, home, away, home_score, away_score, neutral])
