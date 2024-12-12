FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main

COPY . .

RUN chmod a+x docker-entrypoint.sh

