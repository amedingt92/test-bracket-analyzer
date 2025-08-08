import pandas as pd

from src.simulation import features


def test_head_to_head_features_diff():
    df = pd.DataFrame([
        {"team_id": "A", "adj_o": 110.0, "adj_d": 95.0},
        {"team_id": "B", "adj_o": 105.0, "adj_d": 100.0},
    ])
    diff = features.head_to_head_features(df, "A", "B")
    assert diff["adj_o_diff"] == 5.0
    assert diff["adj_d_diff"] == -5.0
