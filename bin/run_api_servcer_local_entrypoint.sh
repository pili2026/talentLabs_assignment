#!/bin/bash
set -e

echo "📦 Running migrations..."
python manage.py migrate

echo "🌱 Seeding database..."
python manage.py seed

echo "🚀 Starting Django server..."
python manage.py runserver 0.0.0.0:8000
