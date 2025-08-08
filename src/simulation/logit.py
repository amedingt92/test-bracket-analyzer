"""Logistic regression model for predicting win probabilities."""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from typing import Dict, Any


def train_logit(train_df: pd.DataFrame, config: dict) -> Dict[str, Any]:
    """
    Train a logistic regression model on the provided DataFrame.

    The DataFrame must contain a column ``outcome`` (1 if team A won, 0 if lost)
    and feature columns specified by config["features"].
    """
    features = config.get("features", [])
    X = train_df[features]
    y = train_df["outcome"]
    C = config.get("C", 1.0)
    penalty = config.get("regularization", "l2")
    model = LogisticRegression(C=C, penalty=penalty, solver="liblinear")
    model.fit(X, y)
    return {"model": model, "features": features}


def predict_logit_prob(model: dict, feats: pd.Series) -> float:
    """
    Predict probability using a trained logistic regression model.
    """
    m = model["model"]
    features = model["features"]
    X = feats[features].values.reshape(1, -1)
    prob = m.predict_proba(X)[0, 1]
    return float(prob)
