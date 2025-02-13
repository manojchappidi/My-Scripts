#!/bin/bash

# Variables
DB_CONTAINER_NAME=<ADD-DB_CONTAINER_NAME-HERE>
DB_NAME=<ADD-DB_NAME-HERE>
BACKUP_FILE=/tmp/${DB_NAME}_$(date +\%Y-\%m-\%d).sql

# Dump the PostgreSQL database
docker exec $DB_CONTAINER_NAME pg_dump -U postgres $DB_NAME > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://<ADD-Bucket-path-here>/

# Remove local backup file
rm $BACKUP_FILE

#RUN THESE CMDS TO AUTOMATE THE BACKUP DATABASE - 
#cron to schedule this script to run every 7 days. Open the crontab file:
     #   crontab -e
     #   0 2 * * 1 /path/to/backup-db.sh >> /var/log/backup-db.log 2>&1
     #   This will run the backup-db.sh script every Monday at 2 AM and log any output to /var/log/backup-db.log.