"""I/O helper functions for reading/writing YAML and managing directories."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import yaml


def read_yaml(path: Path) -> Dict[str, Any]:
    """Read a YAML file and return a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, obj: Dict[str, Any]) -> None:
    """Write a dictionary to a YAML file."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)


def ensure_dir(path: Path) -> None:
    """Ensure that a directory exists, creating it if necessary."""
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def file_hash(path: Path) -> str:
    """Compute a SHA256 hash of a file's contents."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
