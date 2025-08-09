"""Scraper for Sports-Reference college basketball data.

Placeholder implementation that writes metadata files for each season.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import json
import time
import datetime

from ..utils import io as uio


def scrape_sportsref(seasons: List[int], raw_dir: Path, providers_cfg: Dict) -> None:
    base_url = providers_cfg.get("base_url", "")
    delay = providers_cfg.get("politeness_delay_sec", 0)
    for season in seasons:
        season_dir = raw_dir / str(season) / "sportsref"
        uio.ensure_dir(season_dir)
        metadata = {
            "source": "sportsref",
            "season": season,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "base_url": base_url,
        }
        with open(season_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        time.sleep(delay)
