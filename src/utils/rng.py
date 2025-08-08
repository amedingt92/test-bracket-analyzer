"""Random number generator utilities."""

import numpy as np
import random
from typing import Any


def seed_everything(seed: int) -> None:
    """Seed python and numpy RNGs for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)


def get_rng(seed: int) -> np.random.Generator:
    """Get a NumPy random Generator seeded deterministically."""
    return np.random.default_rng(seed)
