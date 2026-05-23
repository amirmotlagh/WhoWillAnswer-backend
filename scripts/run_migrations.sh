#!/bin/bash
set -e

# echo "Waiting for PostgreSQL..."
# until nc -z postgres 5432; do
#   echo "PostgreSQL is unavailable - sleeping"
#   sleep 2
# done
# echo "PostgreSQL is ready"

echo "Running Alembic migrations..."

# Configuration
MAX_MIGRATION_RETRIES=${MAX_MIGRATION_RETRIES:-5}
INITIAL_DELAY=${MIGRATION_INITIAL_DELAY:-2}
MAX_DELAY=${MIGRATION_MAX_DELAY:-30}

attempt=1
delay=$INITIAL_DELAY

while [ $attempt -le $MAX_MIGRATION_RETRIES ]; do
  echo "Migration attempt $attempt of $MAX_MIGRATION_RETRIES..."
  
  if alembic upgrade head; then
    echo "Migrations completed successfully"
    break
  else
    exit_code=$?
    echo "Migration attempt $attempt failed with exit code $exit_code"
    
    if [ $attempt -eq $MAX_MIGRATION_RETRIES ]; then
      echo "ERROR: Migration failed after $MAX_MIGRATION_RETRIES attempts"
      exit 1
    fi
    
    echo "Retrying in ${delay}s..."
    sleep $delay
    
    # Exponential backoff with cap
    delay=$((delay * 2))
    if [ $delay -gt $MAX_DELAY ]; then
      delay=$MAX_DELAY
    fi
    
    attempt=$((attempt + 1))
  fi
done

echo "Starting application..."
exec "$@"