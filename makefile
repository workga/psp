VENV=.venv
DB_URL=postgresql://postgres:postgres@localhost:9432/postgres

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

db-migration: docker-db
	DB_URL=$(DB_URL) $(VENV)/bin/alembic revision --autogenerate

prepare-db: docker-db
	DB_URL=$(DB_URL) $(VENV)/bin/alembic upgrade head

.PHONY: backend
backend: prepare-db
	DB_URL=$(DB_URL) $(VENV)/bin/uvicorn --host localhost --port 9080 --reload --factory backend.app.app:create_app

.PHONY: frontend
frontend:
	PORT=9000 npm start --prefix ./frontend
