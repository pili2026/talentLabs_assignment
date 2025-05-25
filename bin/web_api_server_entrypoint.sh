#!/bin/bash
set -e

echo "Waiting for PostgreSQL ($DB_HOST:$DB_PORT)..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done
echo "PostgreSQL is ready"

echo "Running migrations..."
python manage.py migrate

echo "Seeding database..."
python manage.py seed

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
