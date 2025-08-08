from src.evaluation import bracket_scoring


def test_bracket_scoring_basic():
    picks = {"g1": "A", "g2": "B"}
    truth = {"g1": "A", "g2": "C"}
    config = {"systems": {"espn": {"round_points": [10, 20, 40, 80, 160, 320]}}}
    score = bracket_scoring.score_bracket(picks, truth, "espn", config)
    assert score == 1
