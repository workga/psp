VENV=.venv

init:
	python -m venv $(VENV)
	. $(VENV)/bin/activate && \
	pip install poetry && \
	poetry install
