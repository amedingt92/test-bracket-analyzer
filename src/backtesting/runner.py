"""Backtesting runner implementing different training/testing protocols."""

from __future__ import annotations

import os
import random
from pathlib import Path
from typing import List

import pandas as pd

from ..utils import io as uio


def run_backtest(seasons: List[int], protocol: str, models: List[str], systems: List[str], export_dir: str, seed: int) -> None:
    """
    Run backtests over the specified seasons using the given protocol and models.

    This placeholder implementation generates synthetic metrics for each model
    and season and writes them to a CSV file in the export directory.
    """
    random.seed(seed)
    export_path = Path(export_dir)
    uio.ensure_dir(export_path)
    rows = []
    for season in seasons:
        for model in models:
            rows.append(
                {
                    "season": season,
                    "model": model,
                    "brier": round(random.uniform(0.15, 0.25), 3),
                    "log_loss": round(random.uniform(0.5, 0.7), 3),
                    "auc_roc": round(random.uniform(0.6, 0.8), 3),
                }
            )
    df = pd.DataFrame(rows)
    summary_file = export_path / "backtest_summary.csv"
    df.to_csv(summary_file, index=False)
