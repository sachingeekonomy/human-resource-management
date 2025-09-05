#!/bin/bash

# Wait for database to be ready
echo "Waiting for database connection..."
python manage.py migrate --run-syncdb

# Start the application
echo "Starting application..."
exec gunicorn ems.wsgi:application
