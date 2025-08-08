"""Evaluation metrics for classification probabilities."""

import numpy as np
from sklearn.metrics import log_loss as sk_log_loss, roc_auc_score


def brier_score(p: np.ndarray, y: np.ndarray) -> float:
    """Compute the Brier score."""
    return float(np.mean((p - y) ** 2))


def log_loss(p: np.ndarray, y: np.ndarray) -> float:
    """Compute the log loss (cross-entropy)."""
    # Add small epsilon to avoid log(0)
    eps = 1e-15
    p = np.clip(p, eps, 1 - eps)
    return float(sk_log_loss(y, p))


def auc_roc(p: np.ndarray, y: np.ndarray) -> float:
    """Compute the area under the ROC curve."""
    try:
        return float(roc_auc_score(y, p))
    except ValueError:
        # If only one class present, AUC is undefined; return nan
        return float('nan')
