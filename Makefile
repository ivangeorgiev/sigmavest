.PHONY: install test coverage format lint

# Install dependencies
install:
	poetry install

# Run tests with pytest
test:
	poetry run pytest

# Run tests with coverage
coverage:
	poetry run pytest --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=70 -v

# Format code with black
format:
	poetry run black src tests

# Lint code with ruff
lint:
	poetry run ruff check src tests
