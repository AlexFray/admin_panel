#!/bin/sh
set -e

# chown www-data:www-data /var/log

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done
echo "PostgreSQL started"

echo "Create sсhema..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE SCHEMA IF NOT EXISTS $DB_SCHEMA;"
echo "Start of migrations..."
python manage.py migrate
echo "Completing migrations."

uwsgi --strict --ini ./uwsgi.ini