#!/bin/bash
set -euo pipefail

# Trap errors and provide context
trap 'echo "ERROR: Script failed at line $LINENO with exit code $?" >&2' ERR

echo "=========================================="
echo "Starting custom initialization script"
echo "=========================================="

# ---------- Input validation ----------
if [[ -z "${DATABASE_USERNAME:-}" ]]; then
    echo "ERROR: DATABASE_USERNAME is not set" >&2
    exit 1
fi

if [[ -z "${DATABASE_NAME:-}" ]]; then
    echo "ERROR: DATABASE_NAME is not set" >&2
    exit 1
fi

if [[ -z "${DATABASE_PASSWORD:-}" ]]; then
    echo "ERROR: DATABASE_PASSWORD is not set" >&2
    exit 1
fi

if [[ -z "${POSTGRES_USER:-}" ]]; then
    echo "ERROR: POSTGRES_USER is not set" >&2
    exit 1
fi

if [[ -z "${POSTGRES_DB:-}" ]]; then
    echo "ERROR: POSTGRES_DB is not set" >&2
    exit 1
fi

# Validate identifier format (alphanumeric, underscore, max 63 chars)
if ! [[ "$DATABASE_USERNAME" =~ ^[a-zA-Z_][a-zA-Z0-9_]{0,62}$ ]]; then
    echo "ERROR: DATABASE_USERNAME contains invalid characters or is too long" >&2
    exit 1
fi

if ! [[ "$DATABASE_NAME" =~ ^[a-zA-Z_][a-zA-Z0-9_]{0,62}$ ]]; then
    echo "ERROR: DATABASE_NAME contains invalid characters or is too long" >&2
    exit 1
fi

echo "DATABASE_USERNAME: ${DATABASE_USERNAME}"
echo "DATABASE_NAME: ${DATABASE_NAME}"
echo "=========================================="

# ---------- 1. Create role ----------
echo "Creating/updating role ${DATABASE_USERNAME}..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
       IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DATABASE_USERNAME}') THEN
           CREATE ROLE ${DATABASE_USERNAME} WITH LOGIN PASSWORD '${DATABASE_PASSWORD}';
           RAISE NOTICE 'Created role ${DATABASE_USERNAME}';
       ELSE
           ALTER ROLE ${DATABASE_USERNAME} WITH LOGIN PASSWORD '${DATABASE_PASSWORD}';
           RAISE NOTICE 'Updated role ${DATABASE_USERNAME}';
       END IF;
    END
    \$\$;
EOSQL

if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to create/update role ${DATABASE_USERNAME}" >&2
    exit 1
fi

echo "Role ${DATABASE_USERNAME} ready"

# ---------- 2. Create database ----------
echo "Creating database ${DATABASE_NAME}..."

# Check if database already exists
DB_EXISTS=$(psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${DATABASE_NAME}'")

if [[ "$DB_EXISTS" == "1" ]]; then
    echo "Database ${DATABASE_NAME} already exists, skipping creation"
else
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE DATABASE ${DATABASE_NAME} 
            WITH OWNER = ${DATABASE_USERNAME}
            ENCODING = 'UTF8'
            LC_COLLATE = 'en_US.utf8'
            LC_CTYPE = 'en_US.utf8'
            TEMPLATE = template0;
EOSQL

    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to create database ${DATABASE_NAME}" >&2
        exit 1
    fi
    
    echo "Database ${DATABASE_NAME} created successfully"
fi

# ---------- 3. Grant permissions ----------
echo "Granting permissions to ${DATABASE_USERNAME}..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${DATABASE_NAME}" <<-EOSQL
    -- Revoke public schema access from PUBLIC role for security
    REVOKE CREATE ON SCHEMA public FROM PUBLIC;
    
    -- Grant database-level privileges
    GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DATABASE_USERNAME};
    
    -- Grant schema-level privileges
    GRANT ALL PRIVILEGES ON SCHEMA public TO ${DATABASE_USERNAME};
    
    -- Grant privileges on existing objects
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DATABASE_USERNAME};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DATABASE_USERNAME};
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ${DATABASE_USERNAME};
    
    -- Set default privileges for future objects
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DATABASE_USERNAME};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DATABASE_USERNAME};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO ${DATABASE_USERNAME};
EOSQL

if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to grant permissions to ${DATABASE_USERNAME}" >&2
    exit 1
fi

echo "Permissions granted to ${DATABASE_USERNAME}"

# ---------- 4. Verify setup ----------
echo "Verifying setup..."

VERIFY_ROLE=$(psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -tAc \
    "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname='${DATABASE_USERNAME}'")

VERIFY_DB=$(psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -tAc \
    "SELECT 1 FROM pg_database WHERE datname='${DATABASE_NAME}'")

if [[ "$VERIFY_ROLE" != "1" ]] || [[ "$VERIFY_DB" != "1" ]]; then
    echo "ERROR: Verification failed - role or database not found" >&2
    exit 1
fi

echo "Verification successful"
echo "=========================================="
echo "Initialization script completed successfully"
echo "=========================================="