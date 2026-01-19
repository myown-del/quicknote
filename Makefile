.PHONY: venv sync start start-db start-background build test migration migrate

UV ?= uv

venv:
	$(UV) sync

sync:
	$(UV) sync

start:
	docker compose -f docker-compose.yml up --force-recreate --remove-orphans

start-db:
	docker compose -f docker-compose.yml up postgres -d

start-background:
	docker compose -f docker-compose.yml up -d --force-recreate --remove-orphans

build:
	docker compose -f docker-compose.yml build

test:
	$(UV) run pytest tests --disable-warnings -s

migration:
	$(UV) run alembic revision --autogenerate

migrate:
	$(UV) run alembic upgrade head