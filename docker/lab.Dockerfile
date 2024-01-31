FROM python:3.10-slim

RUN pip install "poetry==1.7.1"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --with play,dev

RUN playwright install firefox && playwright install-deps

WORKDIR /app