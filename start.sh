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

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start the application
echo "Starting application..."
echo "Port: $PORT"
exec gunicorn ems.wsgi:application --bind 0.0.0.0:${PORT:-8000} --timeout 120
