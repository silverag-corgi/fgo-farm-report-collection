help:
	@grep "^[a-zA-Z\-]*:" Makefile | grep -v "grep" | sed -e 's/^/make /' | sed -e 's/://'

install:
	@echo -------------------- install packages ----------------------------------------------------
	@poetry install

update:
	@echo -------------------- update packages -----------------------------------------------------
	@poetry update

lint:
	@echo -------------------- run ruff ------------------------------------------------------------
	@poetry run ruff check . --exit-zero
	@poetry run ruff check . --statistics
	@poetry run ruff format . --check
	@echo -------------------- run mypy ------------------------------------------------------------
	@poetry run mypy .

format:
	@echo -------------------- run ruff ------------------------------------------------------------
	@poetry run ruff check . --fix-only
	@poetry run ruff format .

clean:
	@echo -------------------- clean package -------------------------------------------------------
	@find . | grep .venv$ | xargs rm -fr
	@find . | grep .ruff_cache$ | xargs rm -fr
	@find . | grep .mypy_cache$ | xargs rm -fr
	@find . | grep .pytest_cache$ | xargs rm -fr
	@find . | grep __pycache__$ | xargs rm -fr
