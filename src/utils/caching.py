"""Simple disk caching decorator."""

from __future__ import annotations
from typing import Callable, Any, Dict
import functools
import hashlib
import json
from pathlib import Path


def disk_cache(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that caches function return values on disk.  The cache key is
    computed from the function name and arguments.  Results are stored
    under a `.cache` directory next to the module file.
    """

    cache_dir = Path(__file__).resolve().parent.parent / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key_data = json.dumps({"args": args, "kwargs": kwargs}, default=str, sort_keys=True)
        key_hash = hashlib.sha256(key_data.encode()).hexdigest()
        cache_file = cache_dir / f"{func.__name__}_{key_hash}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        result = func(*args, **kwargs)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(result, f, default=str)
        except Exception:
            pass
        return result

    return wrapper
