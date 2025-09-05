#!/bin/bash

# Wait for database to be ready
echo "Waiting for database connection..."

# Check if DATABASE_URL is available
if [ -z "$DATABASE_URL" ]; then
    echo "No DATABASE_URL found, using SQLite"
    python manage.py migrate
else
    echo "DATABASE_URL found, connecting to PostgreSQL"
    echo "Database URL: $DATABASE_URL"
    python manage.py migrate
fi

# Start the application
echo "Starting application..."
exec gunicorn ems.wsgi:application --bind 0.0.0.0:$PORT
