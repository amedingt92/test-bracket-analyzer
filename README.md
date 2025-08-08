# March Madness Prediction Model

This repository provides a fully reproducible system for building, backtesting and
serving NCAA March Madness predictions.  It uses only free data sources by
default, implements rigorous anti‐leakage safeguards, and exposes a clean
command line interface (CLI) for ingesting historical data, taking snapshots,
training models, generating predictions, running backtests, writing game
previews, and hosting a Streamlit dashboard.

## Features

- **Free data ingestion** from Bart Torvik, Sports‐Reference, NCAA.com and
  Wikipedia with polite delays and disk caching.
- **SQLite database** schemas for teams, games, tournament brackets, seeds,
  metrics, injuries and venues.
- **Configurable feature engineering** including offensive/defensive ratings,
  tempo, strength of schedule, luck, experience proxies, travel distance and
  rest days.
- **Model implementations** for Elo, logistic regression, Bayesian updating
  and a weighted ensemble.  Calibration methods ensure well‐calibrated
  probabilities.
- **Backtesting utilities** implementing leave‐one‐season‐out, expanding and
  fixed window protocols with bracket scoring according to ESPN and Yahoo
  systems.
- **Monte Carlo bracket simulation** and a Streamlit dashboard for interactive
  exploration.
- **Writeups generator** for producing human readable game previews via Jinja2
  templates.
- **Reproducibility manifest** capturing configuration, random seeds, git
  commit and data hashes so that every run can be reproduced.
- **Containerized execution** via a provided Dockerfile and continuous
  integration pipeline.

## Quickstart

First install the dependencies.  Inside this repository run:

```bash
make install
```

Then perform a historical ingest (free sources only):

```bash
python -m src.cli.main ingest --seasons 2010-2024 --providers torvik,sportsref,ncaa,wikipedia
```

Freeze a snapshot at Selection Sunday (no future leakage):

```bash
python -m src.cli.main snapshot --season 2019 --asof 2019-03-17
```

Run a backtest using a leave‐one‐season‐out protocol:

```bash
python -m src.cli.main backtest --seasons 2010-2024 --models elo,logit,bayes,ensemble \
    --protocol loso --scoring_systems espn,yahoo --export outputs/backtests
```

Train models on past seasons and generate predictions for a new season:

```bash
# Freeze as of Selection Sunday 2026
python -m src.cli.main snapshot --season 2026 --asof 2026-03-15

# Train on 2010–2025 data
python -m src.cli.main train --train_seasons 2010-2025 --models elo,logit,bayes,ensemble

# Predict the 2026 bracket
python -m src.cli.main predict --season 2026 --asof 2026-03-15 --export outputs/2026
```

Generate game previews and launch the dashboard:

```bash
python -m src.cli.main writeups --season 2026 --asof 2026-03-15 --style stats-heavy --export outputs/2026/writeups
python -m src.cli.main dashboard --serve
```

## Data Sources and Terms of Service

By default this project uses only free, publicly available data sources: Bart
Torvik (torvik), Sports‐Reference (sportsref), NCAA.com (ncaa) and Wikipedia
(wikipedia).  Each provider can be configured or disabled via
`config/providers.yaml`.  You are responsible for complying with each site’s
terms of service.  A KenPom code path is present but disabled by default
because it requires a subscription; enabling it is optional (see below).

## Enabling KenPom (optional)

The configuration file `config/providers.yaml` includes a `kenpom` entry with
`enabled: false`.  To use KenPom data you must supply your own subscription
credentials and set `enabled: true` in `providers.yaml`.  **Do not enable
KenPom by default**, and do not rely on it in automated tests.  When
enabled, the feature‐engineer and model code will incorporate KenPom metrics as
additional features.

## Reproducibility

All random processes use seeded RNGs.  Snapshot manifests record the exact
versions of data, config and code used for a given run, along with a git
commit hash.  This makes it possible to reproduce any reported result.

## Roadmap

Planned enhancements include refining the feature set and scaling, expanding
the venue geography CSV, adding a public pick distribution scraper for pool
simulations, tuning ensemble weights via cross‐validation, and adding
reliability plots to the calibration reports.

## License

This project is licensed under the MIT license.  See the [LICENSE](LICENSE)
file for details.
