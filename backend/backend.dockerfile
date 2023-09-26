FROM python:3.11

RUN python -m pip install --upgrade pip && \
	python -m pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY makefile ./

EXPOSE 8080
ENTRYPOINT ["make", "backend"]