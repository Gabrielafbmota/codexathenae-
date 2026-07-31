.PHONY: install lint format typecheck test test-unit test-integration test-contract run

install:
	pip install -e ".[dev]"

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	pyright src/

test-unit:
	pytest tests/unit/ tests/contract/ -v

test-integration:
	pytest tests/integration/ -v

test:
	pytest tests/unit/ tests/contract/ tests/integration/ -v

run:
	uvicorn codexathenae.main:app --reload --host 0.0.0.0 --port 8000 --log-config none
