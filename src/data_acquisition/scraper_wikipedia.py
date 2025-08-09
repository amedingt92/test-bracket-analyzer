"""
Mock scraper for Wikipedia data.

This placeholder writes synthetic game and team data.  In a real scraper
you would query Wikipedia pages for tournament results and parse the tables.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import List, Dict, Any


def scrape_wikipedia(seasons: List[int], raw_dir: Path, config: Dict[str, Any]) -> None:
    """Generate dummy data for Wikipedia."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    for season in seasons:
        games_path = raw_dir / f"{season}_games.csv"
        teams_path = raw_dir / f"{season}_teams.csv"
        teams = [f"WP{idx}" for idx in range(1, 5)]
        with teams_path.open("w", newline="", encoding="utf-8") as tf:
            writer = csv.writer(tf)
            writer.writerow(["team_id", "name"])
            for t in teams:
                writer.writerow([t, f"Wiki {t}"])
        with games_path.open("w", newline="", encoding="utf-8") as gf:
            writer = csv.writer(gf)
            writer.writerow(["date", "home_team_id", "away_team_id", "home_score", "away_score", "neutral"])
            for home in teams:
                for away in teams:
                    if home == away:
                        continue
                    date = f"{season}-04-{random.randint(1, 28):02d}"
                    home_score = random.randint(60, 90)
                    away_score = random.randint(60, 90)
                    neutral = 0
                    writer.writerow([date, home, away, home_score, away_score, neutral])
