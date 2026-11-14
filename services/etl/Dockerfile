FROM python:3.14.10-slim-trixie AS builder

WORKDIR /src

ARG POETRY_VERSION=2.5.1

RUN python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
    && python -m venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-ansi


FROM python:3.14.10-slim-trixie AS runtime

WORKDIR /src

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv

COPY src/ ./

ENTRYPOINT ["python", "main.py"]
