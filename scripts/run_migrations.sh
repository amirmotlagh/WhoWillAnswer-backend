#!/bin/bash
set -e

# echo "Waiting for PostgreSQL..."
# until nc -z postgres 5432; do
#   echo "PostgreSQL is unavailable - sleeping"
#   sleep 2
# done
# echo "PostgreSQL is ready"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"