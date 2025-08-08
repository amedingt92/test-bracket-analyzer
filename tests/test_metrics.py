import numpy as np

from src.evaluation import metrics


def test_metrics_basic():
    p = np.array([0.8, 0.2, 0.6, 0.4])
    y = np.array([1, 0, 1, 0])
    assert metrics.brier_score(p, y) >= 0
    assert metrics.log_loss(p, y) >= 0
    auc = metrics.auc_roc(p, y)
    assert 0 <= auc <= 1 or np.isnan(auc)
