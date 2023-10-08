VENV = .venv

export DB_URL ?= postgresql://postgres:postgres@localhost:9432/postgres


init-backend:
	python -m venv $(VENV)
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

init-frontend:
	npm install --prefix ./frontend

init: init-backend init-frontend

docker-db:
	docker-compose down -v
	docker-compose up -d db
	docker-compose up -d redis
	sleep 3

migration-%: docker-db
	$(VENV)/bin/alembic revision --autogenerate -m $(subst migration-,,$@)

prepare-db: docker-db
	$(VENV)/bin/alembic upgrade head
	$(VENV)/bin/python -m backend.app.cli init-data

.PHONY: backend
backend: prepare-db
	$(VENV)/bin/uvicorn --host localhost --port 9080 --reload --factory backend.app.app:create_app

.PHONY: frontend
frontend:
	PORT=9000 npm start --prefix ./frontend
