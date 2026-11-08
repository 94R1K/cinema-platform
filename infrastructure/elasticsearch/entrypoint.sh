#!/bin/bash

set -e

/usr/local/bin/docker-entrypoint.sh "$@" &
ES_PID=$!

echo "Ожидание запуска Elasticsearch..."

until curl -fs http://127.0.0.1:9200 >/dev/null 2>&1; do
    sleep 2
done

echo "Elasticsearch готов к работе"


create_index() {
    local index_name="$1"
    local config_file="$2"

    if curl -fs "http://127.0.0.1:9200/${index_name}" >/dev/null 2>&1; then
        echo "Индекс '${index_name}' уже существует"
    else
        echo "Создание индекса '${index_name}'..."

        curl -fsS \
            -X PUT \
            "http://127.0.0.1:9200/${index_name}" \
            -H 'Content-Type: application/json' \
            --data-binary "@${config_file}"

        echo
        echo "Индекс '${index_name}' успешно создан"
    fi
}


create_index \
    "movies" \
    "/usr/share/elasticsearch/config/movies.json"

create_index \
    "genres" \
    "/usr/share/elasticsearch/config/genres.json"

create_index \
    "persons" \
    "/usr/share/elasticsearch/config/persons.json"

wait "$ES_PID"
