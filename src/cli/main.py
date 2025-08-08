"""
Command line interface for the March Madness model.

This module defines a single entry point with subcommands for ingesting data,
taking snapshots, training models, predicting brackets, running backtests,
generating writeups and serving the dashboard.  Each subcommand delegates to
functions in the respective modules under ``src``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from ..utils import io as uio
from ..utils import dates as udates
from ..data_acquisition import schema as schema_mod
from ..data_acquisition import etl as etl_mod
from ..data_acquisition import scraper_torvik, scraper_sportsref, scraper_ncaa, scraper_wikipedia  # type: ignore
from ..data_cleaning import standardize, join_features, leakage_guards
from ..simulation import elo, logit, bayes, ensemble, calibration, monte_carlo, features as feat_mod
from ..evaluation import metrics as eval_metrics, bracket_scoring, pool_simulator, reports  # type: ignore
from ..backtesting import runner as backtest_runner
from ..visualization import dashboard_streamlit
from ..writeups import generator as writeups_gen


def _parse_season_range(season_range: str) -> List[int]:
    """Parse a season range string like "2010-2024" into a list of ints."""
    if '-' in season_range:
        start, end = season_range.split('-', 1)
        return list(range(int(start), int(end) + 1))
    else:
        return [int(season_range)]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="March Madness prediction CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Ingest subcommand
    p_ingest = subparsers.add_parser("ingest", help="Ingest raw data for seasons")
    p_ingest.add_argument("--seasons", required=True, help="Season range, e.g. 2010-2024")
    p_ingest.add_argument("--providers", required=True, help="Comma separated provider list")

    # Snapshot subcommand
    p_snapshot = subparsers.add_parser("snapshot", help="Freeze data as of a given date")
    p_snapshot.add_argument("--season", type=int, required=True, help="Season year")
    p_snapshot.add_argument("--asof", required=True, help="As-of date YYYY-MM-DD")

    # Train subcommand
    p_train = subparsers.add_parser("train", help="Train models on historical seasons")
    p_train.add_argument("--train_seasons", required=True, help="Range of seasons for training")
    p_train.add_argument("--models", required=True, help="Comma separated list of models to train")

    # Predict subcommand
    p_predict = subparsers.add_parser("predict", help="Generate predictions for a season")
    p_predict.add_argument("--season", type=int, required=True, help="Season year to predict")
    p_predict.add_argument("--asof", required=True, help="As-of date YYYY-MM-DD")
    p_predict.add_argument("--export", required=True, help="Export directory for predictions")

    # Backtest subcommand
    p_backtest = subparsers.add_parser("backtest", help="Run backtests across seasons")
    p_backtest.add_argument("--seasons", required=True, help="Season range for backtesting")
    p_backtest.add_argument("--models", required=True, help="Comma separated model list")
    p_backtest.add_argument("--protocol", required=True, choices=["loso", "expanding", "fixed"], help="Backtest protocol")
    p_backtest.add_argument("--scoring_systems", required=True, help="Comma separated scoring systems")
    p_backtest.add_argument("--export", required=True, help="Directory to export backtest results")

    # Writeups subcommand
    p_writeups = subparsers.add_parser("writeups", help="Generate game preview writeups")
    p_writeups.add_argument("--season", type=int, required=True)
    p_writeups.add_argument("--asof", required=True)
    p_writeups.add_argument("--style", required=True, help="Writeup style (e.g. stats-heavy)")
    p_writeups.add_argument("--export", required=True, help="Export directory for writeups")

    # Dashboard subcommand
    p_dashboard = subparsers.add_parser("dashboard", help="Run or build the dashboard")
    p_dashboard.add_argument("--serve", action="store_true", help="Serve the dashboard (default)")
    p_dashboard.add_argument("--build-static", action="store_true", help="Build static assets instead of serving")

    args = parser.parse_args(argv)

    # Load base configuration
    base_cfg = uio.read_yaml(Path(__file__).resolve().parent.parent.parent / "config" / "base.yaml")
    providers_cfg = uio.read_yaml(Path(__file__).resolve().parent.parent.parent / "config" / "providers.yaml")

    if args.command == "ingest":
        seasons = _parse_season_range(args.seasons)
        providers = [p.strip() for p in args.providers.split(',') if p.strip()]
        raw_dir = Path(base_cfg["raw_dir"])
        # ensure directories exist
        uio.ensure_dir(raw_dir)
        # initialise database
        db_path = Path(base_cfg["processed_dir"]) / "mm.db"
        uio.ensure_dir(db_path.parent)
        schema_mod.init_db(str(db_path))
        # scrape each provider
        for prov in providers:
            if prov == "torvik":
                scraper_torvik.scrape_torvik(seasons, raw_dir, providers_cfg["sources"]["torvik"])  # type: ignore[attr-defined]
            elif prov == "sportsref":
                scraper_sportsref.scrape_sportsref(seasons, raw_dir, providers_cfg["sources"]["sportsref"])  # type: ignore[attr-defined]
            elif prov == "ncaa":
                scraper_ncaa.scrape_ncaa(seasons, raw_dir, providers_cfg["sources"]["ncaa"])  # type: ignore[attr-defined]
            elif prov == "wikipedia":
                scraper_wikipedia.scrape_wikipedia(seasons, raw_dir, providers_cfg["sources"]["wikipedia"])  # type: ignore[attr-defined]
            else:
                print(f"Unknown provider: {prov}", file=sys.stderr)
        # ingest raw to sqlite
        etl_mod.ingest_to_sqlite(seasons, raw_dir, str(db_path))
        etl_mod.index_db(str(db_path))
        print("Ingestion complete")

    elif args.command == "snapshot":
        season = args.season
        asof = args.asof
        db_path = Path(base_cfg["processed_dir"]) / "mm.db"
        # Standardize names and compute experience etc.
        standardize.standardize_team_names(str(db_path))
        standardize.compute_experience_proxy(str(db_path))
        # Build feature table and apply leakage guards
        join_features.build_feature_table(str(db_path), season, asof)
        leakage_guards.assert_no_post_asof_rows(str(db_path), season, asof)
        leakage_guards.assert_feature_dates_valid(str(db_path), season, asof)
        print(f"Snapshot for season {season} as of {asof} created")

    elif args.command == "train":
        train_seasons = _parse_season_range(args.train_seasons)
        models = [m.strip() for m in args.models.split(',') if m.strip()]
        # Placeholder: training loop would load data and fit models
        print(f"Training models {models} on seasons {train_seasons}")
        # TODO: implement actual training using simulation modules

    elif args.command == "predict":
        season = args.season
        asof = args.asof
        export = Path(args.export)
        uio.ensure_dir(export)
        # Placeholder: run predictions
        print(f"Predicting season {season} as of {asof} to {export}")
        # TODO: implement actual prediction generation and export

    elif args.command == "backtest":
        seasons = _parse_season_range(args.seasons)
        models = [m.strip() for m in args.models.split(',') if m.strip()]
        protocol = args.protocol
        systems = [s.strip() for s in args.scoring_systems.split(',') if s.strip()]
        export_dir = args.export
        backtest_runner.run_backtest(seasons, protocol, models, systems, export_dir, seed=base_cfg["random_seed"])
        print("Backtest completed")

    elif args.command == "writeups":
        season = args.season
        asof = args.asof
        style = args.style
        export = Path(args.export)
        uio.ensure_dir(export)
        template_dir = Path(__file__).resolve().parent.parent / "writeups" / "templates"
        writeups_gen.generate_game_writeups(season, asof, style, base_cfg["db_path"], template_dir, export)
        print("Writeups generated")

    elif args.command == "dashboard":
        db_path = base_cfg["db_path"]
        snapshots_dir = base_cfg["snapshots_dir"]
        if args.build_static:
            print("Building static dashboard is not implemented yet")
        else:
            dashboard_streamlit.run_dashboard(db_path, snapshots_dir)

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
