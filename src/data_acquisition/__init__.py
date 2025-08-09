"""Data acquisition subpackage.

This subpackage contains modules for defining the SQLite database schema,
ingesting raw scraped data into the database and (in a full implementation)
scraping data from external sources.

Modules
-------
schema
    Defines the SQLite database schema and a helper for initialising the DB.
etl
    Provides functions for ingesting raw CSV files and creating indices.
scraper_torvik, scraper_sportsref, scraper_ncaa, scraper_wikipedia
    Mock scraper implementations that generate synthetic datasets.  Replace
    these with real scrapers that fetch and parse data from the respective
    providers.
"""

from . import schema
from . import etl
from . import scraper_torvik
from . import scraper_sportsref
from . import scraper_ncaa
from . import scraper_wikipedia

__all__ = [
    "schema",
    "etl",
    "scraper_torvik",
    "scraper_sportsref",
    "scraper_ncaa",
    "scraper_wikipedia",
]
