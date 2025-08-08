"""Functions for blending probabilities from multiple models."""

from typing import Dict, List


def blend_probs(probs: Dict[str, float], method: str = "weighted", weights: List[float] | None = None) -> float:
    """
    Blend probabilities from multiple models into a single probability.

    Parameters
    ----------
    probs : dict
        Mapping from model name to predicted probability.
    method : str
        Method to combine probabilities.  Only 'weighted' is currently supported.
    weights : list, optional
        Weights corresponding to the models.  If None, equal weights are used.

    Returns
    -------
    float
        Blended probability.
    """
    names = list(probs.keys())
    values = [probs[name] for name in names]
    if method != "weighted":
        raise ValueError(f"Unknown ensemble method {method}")
    if weights is None:
        weights = [1.0 / len(values)] * len(values)
    else:
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
    return float(sum(w * p for w, p in zip(weights, values)))
