FROM python:3.11-slim

ENV POETRY_VERSION 1.5.1
WORKDIR /app

# for install geopandas
RUN apt-get update \
    && apt-get install -y --no-install-recommends  \
    gdal-bin \
    libgdal-dev \
    build-essential
ENV GDAL_CONFIG /usr/bin/gdal-config

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

# fastapi / celery
COPY ./ /app
ENV PYTHONPATH=/app/src
CMD ["poetry", "run", "celery", "-A", "src.fast_api.worker.predict_worker", "worker", "-l", "INFO"]
