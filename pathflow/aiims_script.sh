#!/bin/bash
# Log file path
LOG_FILE="/var/log/aiims_script.log"
# Function to log messages
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" >> "$LOG_FILE"
}
# Redirect all output to log file
exec >> "$LOG_FILE" 2>&1
# Log start of script
log_message "Starting AIIMS Script"
# Stop and Start Docker Containers using Docker Compose
log_message "Stopping Docker containers"
sudo docker-compose down
log_message "Starting Docker containers"
sudo docker-compose up -d
# Configure MinIO
log_message "Configuring MinIO"
sudo mc admin config set myminio api cors_allow_origin=https://aiims.pathflowdx.com
# List Docker Containers
log_message "Listing Docker containers"
sudo docker ps -a
# Log end of script
log_message "AIIMS Script completed"