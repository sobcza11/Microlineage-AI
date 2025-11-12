.PHONY: setup lint fmt test all

setup:
	python -m pip install --upgrade pip
	if exist requirements-dev.txt (pip install -r requirements-dev.txt)
	if exist pyproject.toml (pip install -e . || echo editable install skipped)

lint:
	ruff check .
	black --check .

fmt:
	ruff check . --fix
	black .

test:
	set PYTHONPATH=.;_supporting;_supporting\src && pytest --maxfail=1 --disable-warnings

all: setup lint test
