export DB_HOST=localhost && \
export DB_NAME=cardpay-dev-db && \
export DB_USER=postgres && \
export DB_PASSWORD="-3vjMTP4s>*aEDuG" && \
export DB_PORT=5433 && \

export DB_MIN_CON=1
export DB_MAX_CON=1

flask --app core.api.api:app --debug run