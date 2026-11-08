#!/usr/bin/env bash

set -Eeuo pipefail

: "${POSTGRES_DATABASES:?POSTGRES_DATABASES требуется}"
: "${POSTGRES_USER:?POSTGRES_USER требуется}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD требуется}"

export PGPASSWORD="$POSTGRES_PASSWORD"

read -r -a services <<< "$POSTGRES_DATABASES"

for service in "${services[@]}"; do
    name_var="DB_${service}_NAME"
    user_var="DB_${service}_USER"
    password_var="DB_${service}_PASSWORD"

    db_name="${!name_var:?Отсутствует $name_var}"
    db_user="${!user_var:?Отсутствует $user_var}"
    db_password="${!password_var:?Отсутствует $password_var}"

    echo "Подготовка базы данных: $db_name"

    DB_NAME="$db_name" \
    DB_USER="$db_user" \
    DB_PASSWORD="$db_password" \
    psql \
        --host=127.0.0.1 \
        --port="${PGPORT:-5432}" \
        --username="$POSTGRES_USER" \
        --dbname=postgres \
        --no-psqlrc \
        --set=ON_ERROR_STOP=1 \
        --file=/scripts/create-databases.sql
done

echo "Все базы данных успешно развернуты"
