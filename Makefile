PYTHON = uv run python
MANAGE = $(PYTHON) manage.py
SETTINGS = task_manager.settings


install:
	uv sync

dev-install:
	uv sync --group dev

build:
	./build.sh

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

collectstatic:
	$(MANAGE) collectstatic --noinput

run:
	uv run python manage.py runserver

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	python manage.py loaddata users.json && make test
	uv run pytest --ds=$(SETTINGS) --reuse-db -xvs

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=$(SETTINGS) --reuse-db
	uv run coverage report --show-missing --skip-covered
	uv run coverage html

ci-install:
	uv sync --group dev

ci-migrate:
	$(MANAGE) migrate --noinput

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=$(SETTINGS)
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered

ci: ci-install ci-migrate ci-test

.PHONY: install dev-install migrate makemigrations collectstatic run lint lint-fix test coverage ci-install ci-migrate ci-test ci
