from pathlib import Path

from src.data_acquisition import scraper_torvik, scraper_sportsref, scraper_ncaa, scraper_wikipedia


def test_scrapers_create_metadata(tmp_path):
    seasons = [2020]
    raw_dir = tmp_path
    providers_cfg = {"base_url": "", "politeness_delay_sec": 0}
    # Torvik
    scraper_torvik.scrape_torvik(seasons, raw_dir, providers_cfg)
    assert (raw_dir / "2020" / "torvik" / "metadata.json").exists()
    # Sportsref
    scraper_sportsref.scrape_sportsref(seasons, raw_dir, providers_cfg)
    assert (raw_dir / "2020" / "sportsref" / "metadata.json").exists()
    # NCAA
    scraper_ncaa.scrape_ncaa(seasons, raw_dir, providers_cfg)
    assert (raw_dir / "2020" / "ncaa" / "metadata.json").exists()
    # Wikipedia
    scraper_wikipedia.scrape_wikipedia(seasons, raw_dir, providers_cfg)
    assert (raw_dir / "2020" / "wikipedia" / "metadata.json").exists()
