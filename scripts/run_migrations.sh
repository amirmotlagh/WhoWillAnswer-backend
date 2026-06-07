#!/bin/bash
set -e

if [[ "$MIGRATE" != "True" ]] ; then
  echo "MIGRATE is not set to 'True', skipping migrations"
  exec "$@"
fi

DB_READY_TIMEOUT=${DB_READY_TIMEOUT:-60}
start_time=$(date +%s)
PYTHON_CMD=$(command -v python3 || command -v python)

if [ -z "$PYTHON_CMD" ]; then
  echo "ERROR: python or python3 is required for the readiness check"
  exit 1
fi

echo "Waiting for PostgreSQL..."
until $PYTHON_CMD -c "import socket; s = socket.socket(); s.settimeout(2); s.connect(('${DATABASE_HOST:-postgres}', ${DATABASE_PORT:-5432}))" 2>/dev/null; do
  current_time=$(date +%s)
  if [ $((current_time - start_time)) -ge "$DB_READY_TIMEOUT" ]; then
    echo "ERROR: Timed out waiting for PostgreSQL after $DB_READY_TIMEOUT seconds"
    exit 1
  fi
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready"

echo "Running Alembic migrations..."

# Configuration
MAX_MIGRATION_RETRIES=${MAX_MIGRATION_RETRIES:-5}
INITIAL_DELAY=${MIGRATION_INITIAL_DELAY:-3}
MAX_DELAY=${MIGRATION_MAX_DELAY:-30}

if ! [[ "$MAX_MIGRATION_RETRIES" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: MAX_MIGRATION_RETRIES must be a positive integer"
  exit 1
fi

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