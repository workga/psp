VENV=.venv


init-backend:
	python -m venv $(VENV)
	. $(VENV)/bin/activate && \
	pip install poetry && \
	poetry install

init-frontend:
	cd frontend && \
	npm install

init: init-backend init-frontend

app:
	uvicorn --host 0.0.0.0 --port 8000 --reload --factory backend.app.app:create_app
