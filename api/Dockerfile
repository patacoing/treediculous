FROM python:3.10-slim-bullseye AS base

FROM base AS builder

WORKDIR /api
RUN mkdir -p /model

ENV PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1

RUN pip install --user "poetry==${POETRY_VERSION}"
RUN poetry config virtualenvs.in-project true

COPY api/poetry.lock api/pyproject.toml ./
COPY model /model

RUN poetry install --sync --no-cache

FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/api/.venv/bin:${PATH}

WORKDIR /api

COPY --from=builder /api/.venv/ /api/.venv/
COPY api/ .

EXPOSE 8000

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]