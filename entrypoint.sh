#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Function to check if Postgres is ready
postgres_ready() {
    python << END
import sys
import psycopg2
from urllib.parse import urlparse
try:
    result = urlparse("${DATABASE_URL}")
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

# Wait for PostgreSQL to become available
until postgres_ready; do
  echo >&2 "Waiting for PostgreSQL to become available..."
  sleep 1
done
echo >&2 "PostgreSQL is available"

# Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create cache tables
echo "Creating cache tables..."
python manage.py createcachetable

# Start Gunicorn
echo "Starting Gunicorn..."

TIMEOUT=120
PORT=4000

exec python -m gunicorn config.asgi:application \
    -k uvicorn_worker.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout $TIMEOUT \
    --keep-alive 60 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --log-level=info \
    --access-logfile - \
    --error-logfile -
