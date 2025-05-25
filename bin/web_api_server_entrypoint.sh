#!/bin/bash
set -e

echo "Waiting for database..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
