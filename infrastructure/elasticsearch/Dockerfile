FROM docker.elastic.co/elasticsearch/elasticsearch:9.5.1

USER root

COPY --chown=elasticsearch:elasticsearch index_configs/movies.json /usr/share/elasticsearch/config/movies.json
COPY --chown=elasticsearch:elasticsearch index_configs/genres.json /usr/share/elasticsearch/config/genres.json
COPY --chown=elasticsearch:elasticsearch index_configs/persons.json /usr/share/elasticsearch/config/persons.json

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER elasticsearch

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
