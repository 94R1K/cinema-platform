FROM python:3.14.10-slim-trixie

WORKDIR /tests

ARG POETRY_VERSION=2.5.1

ENV POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/poetry/bin:/tests/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION} \
    && /opt/poetry/bin/poetry --version \
    && rm -rf /var/lib/apt/lists/*

COPY functional/pyproject.toml functional/poetry.lock ./

RUN poetry install --only main --no-root

COPY functional/ ./
COPY core/ ./core

CMD ["python", "-m", "pytest", "-v", "src"]
