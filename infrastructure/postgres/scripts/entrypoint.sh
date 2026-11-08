#!/usr/bin/env bash

set -Eeuo pipefail

READY_FILE=/tmp/postgres-provisioned

# Удаляем маркер при каждом запуске контейнера.
rm -f "$READY_FILE"

# Запускаем оригинальный entrypoint PostgreSQL в фоне.
# Он выполнит стандартную инициализацию и запустит PostgreSQL.
/usr/local/bin/docker-entrypoint.sh "$@" &

postgres_pid=$!


# Корректно останавливаем PostgreSQL при завершении wrapper.
stop_postgres() {
    if [[ -n "${postgres_pid:-}" ]]; then
        kill -TERM "$postgres_pid" 2>/dev/null || true
        wait "$postgres_pid" 2>/dev/null || true
    fi
}

trap stop_postgres EXIT
trap 'exit 143' TERM
trap 'exit 130' INT


# Ожидаем готовности PostgreSQL принимать TCP-соединения.
startup_timeout="${POSTGRES_STARTUP_TIMEOUT:-120}"
ready=0

for ((attempt = 0; attempt < startup_timeout; attempt++)); do
    if pg_isready \
        --host=127.0.0.1 \
        --port="${PGPORT:-5432}" \
        --username="${POSTGRES_USER:-postgres}" \
        --dbname=postgres \
        >/dev/null 2>&1
    then
        ready=1
        break
    fi

    sleep 1
done

if [[ "$ready" -ne 1 ]]; then
    echo "PostgreSQL не стал доступен за ${startup_timeout} секунд" >&2
    exit 1
fi


# Выполняем подготовку баз данных и пользователей.
echo "Начинаем подготовку PostgreSQL..."

bash /scripts/provision.sh

# Помечаем успешное завершение подготовки.
touch "$READY_FILE"

echo "Подготовка PostgreSQL успешно завершена"


# Ожидаем завершения основного процесса PostgreSQL.
if wait "$postgres_pid"; then
    status=0
else
    status=$?
fi

postgres_pid=""

exit "$status"
