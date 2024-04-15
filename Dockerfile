FROM python:3.11-slim
ENV POETRY_VERSION 1.5.1
WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

# COPY ./src/app/example.py .
