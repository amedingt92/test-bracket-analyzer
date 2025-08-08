"""Thin wrapper around the standard logging module for project-wide use."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Create and return a logger with a simple format."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
