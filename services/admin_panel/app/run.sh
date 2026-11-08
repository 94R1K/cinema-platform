#!/bin/sh

set -e

python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --worker-class gthread \
    --workers "${GUNICORN_WORKERS}" \
    --threads "${GUNICORN_THREADS}" \
    --timeout "${GUNICORN_TIMEOUT}" \
    --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT}" \
    --max-requests "${GUNICORN_MAX_REQUESTS}" \
    --access-logfile - \
    --error-logfile -
