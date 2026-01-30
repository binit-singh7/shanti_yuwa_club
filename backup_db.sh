#!/bin/bash

# Database Backup Script for Shanti Yuwa Club
# Usage: ./backup_db.sh

# Create backups directory if it doesn't exist
mkdir -p backups

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="backups/db_backup_${TIMESTAMP}.json"

echo "Starting database backup..."
echo "Backup file: $BACKUP_FILE"

# Backup database using Django's dumpdata
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude contenttypes \
    --exclude auth.permission \
    --indent 2 \
    > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Backup completed successfully!"
    echo "Backup saved to: $BACKUP_FILE"
    
    # Keep only last 10 backups
    ls -t backups/db_backup_*.json | tail -n +11 | xargs -r rm
    echo "Old backups cleaned up (keeping last 10)"
else
    echo "✗ Backup failed!"
    exit 1
fi
