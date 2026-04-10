install:
	uv sync
	uv sync --dev

lint:
	uv run flake8 src tests

test:
	uv run pytest

format:
	uv run black src tests
	uv run isort src tests

mypy:
	uv run mypy src

clean:
	rm -rf __pycache__
	rm -rf .venv .env
	rm -rf .pytest_cache .mypy_cache
	rm -rf logs reports
	rm -f .coverage

run:
	uv run python -m src.log_analyzer.main
