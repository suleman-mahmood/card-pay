export DB_HOST=localhost && \
export DB_NAME=cardpay-prod-db && \
export DB_USER=postgres && \
export DB_PASSWORD="b>dX6s5$,+f\@jv6" && \
export DB_PORT=5433 && \

export DB_MIN_CON=1
export DB_MAX_CON=1

flask --app core.api.api:app --debug run