# syntax=docker/dockerfile:1.0.0-experimental
FROM python:alpine as base
ENV AWS_DEFAULT_REGION=us-east-1
RUN apk update && apk add libffi-dev \
    openssl-dev \
    openssh-client \
    gcc \
    python3-dev \
    musl-dev \
    make \
    git
WORKDIR /app
COPY src/setup.py .
RUN pip install .

FROM base as dist

FROM base as test
RUN --mount=type=ssh pip install .[dev,docs]
