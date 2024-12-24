FROM python:3.10-slim-bullseye AS base

FROM base AS builder

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH \
    POETRY_VERSION=1.8.3

RUN pip install --user "poetry==${POETRY_VERSION}"
RUN python -m venv /venv

COPY poetry.lock pyproject.toml ./

RUN . /venv/bin/activate && poetry install -n --sync --no-directory --no-root --with api && poetry run pip install setuptools


FROM base AS final
RUN useradd -r newuser
USER newuser
ENV PATH=/venv/bin:${PATH}

WORKDIR /app

COPY --from=builder /venv /venv
COPY ./app ./app

EXPOSE 8000

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]