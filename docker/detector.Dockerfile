FROM python:3.10-slim

RUN pip install "poetry==1.7.1"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only model

RUN poetry install --no-root --only base

COPY scripts/ scripts/

RUN python3 scripts/download_model.py

WORKDIR /app

COPY detector/ detector/
