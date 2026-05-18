#!/bin/bash
set -e

echo "=========================================="
echo "Starting custom initialization script"
echo "DATABASE_USERNAME: ${DATABASE_USERNAME}"
echo "DATABASE_NAME: ${DATABASE_NAME}"
echo "=========================================="

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- ---------- 1. Create roles ----------
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

    -- ---------- 2. Create databases ----------
    CREATE DATABASE ${DATABASE_NAME};
EOSQL

echo "Database ${DATABASE_NAME} created successfully"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${DATABASE_NAME}" <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE ${DATABASE_NAME} TO ${DATABASE_USERNAME};

    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DATABASE_USERNAME};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DATABASE_USERNAME};
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ${DATABASE_USERNAME};

    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DATABASE_USERNAME};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DATABASE_USERNAME};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO ${DATABASE_USERNAME};
EOSQL

echo "Permissions granted to ${DATABASE_USERNAME}"
echo "=========================================="
echo "Initialization script completed"
echo "=========================================="