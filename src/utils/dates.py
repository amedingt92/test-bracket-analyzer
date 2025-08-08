"""Date utilities used by the March Madness model."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import calendar
from typing import Optional


def selection_sunday(season: int) -> date:
    """
    Estimate the date of Selection Sunday for a given season.

    This implementation finds the Sunday in March between the 11th and 17th
    inclusive (which historically corresponds to Selection Sunday).  It may not
    be exact for all seasons but provides a reasonable default.
    """
    # Find all Sundays in March
    for day in range(11, 18):
        d = date(season, 3, day)
        if d.weekday() == 6:  # Sunday
            return d
    # Fallback: return March 15
    return date(season, 3, 15)


def parse_ymd(s: str) -> date:
    """Parse a YYYY-MM-DD formatted string into a date object."""
    return datetime.strptime(s, "%Y-%m-%d").date()


def ymd(d: date) -> str:
    """Format a date object as YYYY-MM-DD."""
    return d.strftime("%Y-%m-%d")
