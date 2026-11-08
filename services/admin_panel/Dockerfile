FROM python:3.14.10-slim-trixie AS builder

WORKDIR /app

ARG POETRY_VERSION=2.5.1

RUN python -m pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
    && python -m venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-ansi


FROM python:3.14.10-slim-trixie AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

COPY --from=builder /opt/venv /opt/venv

COPY app/ ./

RUN mkdir -p /var/www/static /var/www/media \
    && chown -R www-data:www-data /var/www

USER www-data

EXPOSE 8000


FROM runtime AS development

ENTRYPOINT ["/bin/sh", "/app/run.dev.sh"]


FROM runtime AS production

ENV GUNICORN_WORKERS=1 \
    GUNICORN_THREADS=16 \
    GUNICORN_TIMEOUT=240 \
    GUNICORN_GRACEFUL_TIMEOUT=10 \
    GUNICORN_MAX_REQUESTS=5000

ENTRYPOINT ["/bin/sh", "/app/run.sh"]
