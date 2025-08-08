"""Data acquisition package.

This package contains the schemas, scraping logic and ETL pipelines for
ingesting data from external sources into our SQLite database.
"""

__all__ = [
    "schema",
    "etl",
    "scraper_torvik",
    "scraper_sportsref",
    "scraper_ncaa",
    "scraper_wikipedia",
]
