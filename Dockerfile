# syntax=docker/dockerfile:1.0.0-experimental
FROM python:slim as base
ENV AWS_DEFAULT_REGION=us-east-1
RUN apt update && apt install -y \
    libffi-dev \
    gcc \
    python3-dev \
    musl-dev \
    make \
    git
WORKDIR /app
COPY setup.py .
RUN pip install .

FROM base as dist

FROM base as test
RUN --mount=type=ssh pip install .[dev,docs]
