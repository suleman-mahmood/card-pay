export DB_HOST=localhost && \
export DB_NAME=cardpay && \
export DB_USER=postgres && \
export DB_PASSWORD=root && \
export DB_PORT=5432 && \

flask --app core.api.api:app --debug run