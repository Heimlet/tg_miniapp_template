#!/bin/sh

# Wait for the database to be ready
while ! nc -z db "$POSTGRES_PORT"; do
  echo "Waiting for the database..."
  sleep 1
done

# Ensure the database and user are created
psql -h db -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_USER'" | grep -q 1 || \
  psql -h db -U postgres -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || \
  psql -h db -U postgres -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn and Nginx using the Gunicorn config file
gunicorn tg_miniapp.wsgi:application --config configs/gunicorn.conf.py & nginx -g 'daemon off;'
