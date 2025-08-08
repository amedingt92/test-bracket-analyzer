"""Probability calibration utilities."""

import numpy as np
from sklearn.isotonic import IsotonicRegression
from typing import Dict, Any


def fit_calibrator(probs: np.ndarray, outcomes: np.ndarray, method: str) -> Dict[str, Any]:
    """
    Fit a calibrator using the specified method.
    Supported methods: 'isotonic' (default), 'none'.
    """
    if method == "isotonic":
        iso = IsotonicRegression(out_of_bounds="clip")
        iso.fit(probs, outcomes)
        return {"method": "isotonic", "model": iso}
    else:
        # No calibration
        return {"method": "none"}


def apply_calibrator(probs: np.ndarray, cal: Dict[str, Any]) -> np.ndarray:
    """
    Apply a fitted calibrator to an array of probabilities.
    """
    if cal.get("method") == "isotonic":
        iso: IsotonicRegression = cal["model"]
        return iso.transform(probs)
    else:
        return probs
