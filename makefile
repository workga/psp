VENV=.venv


init-backend:
	python -m venv $(VENV)
	. $(VENV)/bin/activate && \
	pip install poetry && \
	poetry install

init-frontend:
	cd frontend; npm install

init: init-backend init-frontend

.PHONY: backend
backend:
	uvicorn --host 0.0.0.0 --port 8080 --reload --factory backend.app.app:create_app

.PHONY: frontend
frontend:
	cd frontend; PORT=8090 npm start

docker-buid:
	docker-compose build

docker-up:
	docker-compose up
