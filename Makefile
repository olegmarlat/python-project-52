PYTHON = uv run python
MANAGE = $(PYTHON) manage.py
SETTINGS = task_manager.settings


install:
	uv sync

dev-install:
	uv sync --group dev

build:
    ./build.sh

render-start:
    gunicorn task_manager.wsgi

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

collectstatic:
	$(MANAGE) collectstatic --noinput

run:
	$(MANAGE) runserver 0.0.0.0:8000


lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .


test:
	uv run pytest --ds=$(SETTINGS) --reuse-db -xvs

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=$(SETTINGS) --reuse-db
	uv run coverage report --show-missing --skip-covered
	uv run coverage html  # генерирует отчёт в htmlcov/

ci-install:
	uv sync --group dev

ci-migrate:
	$(MANAGE) migrate --noinput

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=$(SETTINGS) --reuse-db
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered

.PHONY: install dev-install migrate makemigrations collectstatic run lint lint-fix test coverage ci-install ci-migrate ci-test


