FROM python:3.10-slim-bullseye AS base

FROM base AS builder

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1

RUN pip install --user "poetry==${POETRY_VERSION}"
RUN poetry config virtualenvs.in-project true

COPY pipeline/poetry.lock pipeline/pyproject.toml ./
COPY model /model

RUN poetry install --sync --no-root && poetry run pip install setuptools


FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/venv/bin:${PATH}

COPY --from=builder /app/.venv /venv