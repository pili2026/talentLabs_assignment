#!/bin/bash

set -e

export CONFIG_YAML=config.test.yml

docker compose -f docker-compose.test.yml up -d

echo "Waiting for Django to be able to connect and migrate..."
MAX_ATTEMPTS=30
attempt=1
until python manage.py migrate --settings=job_platform.settings > /dev/null 2>&1; do
  if [ $attempt -ge $MAX_ATTEMPTS ]; then
    echo "Error: Django could not connect to DB or migrate within timeout."
    docker logs talentlabs_timescaledb_test
    exit 1
  fi
  echo "  Attempt $attempt/$MAX_ATTEMPTS: Waiting for successful migrate..."
  sleep 2
  attempt=$((attempt + 1))
done

echo "Database is ready. Running tests..."
pytest --reuse-db "$@"

docker compose -f docker-compose.test.yml down -v
