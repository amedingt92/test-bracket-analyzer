install:
	pip install -r requirements.txt

lint:
	# Install ruff if not already installed
	python -m pip install ruff
	ruff r src

test:
	# Compute absolute path to the src directory
	PYTHONPATH=$(shell pwd)/src pytest -q

ingest:
	python -m src.cli.main ingest --seasons 2010-2024 --providers torvik,sportsref,ncaa,wikipedia

snapshot:
	python -m src.cli.main snapshot --season 2019 --asof 2019-03-17

backtest:
	python -m src.cli.main backtest --seasons 2010-2024 --models elo,logit,bayes,ensemble --protocol loso --scoring_systems espn,yahoo --export outputs/backtests
