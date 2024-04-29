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

# Snakemake
RUN apt-get -y install graphviz
RUN pip install snakemake

# install package
COPY dist/mlops_ods-0.1.0-py3-none-any.whl .
RUN pip install mlops_ods-0.1.0-py3-none-any.whl
RUN rm mlops_ods-0.1.0-py3-none-any.whl

COPY ./ ./
