#!/bin/bash

# Build script for Render.com
# This script runs during deployment

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Creating superuser..."
python manage.py createsuperuser --no-input 2>/dev/null || echo "Superuser already exists, skipping."

echo "Build complete!"
