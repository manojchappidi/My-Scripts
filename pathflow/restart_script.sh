#!/bin/bash
# Restart Docker containers using docker-compose
sudo docker-compose down
sudo docker-compose up -d
# Check Docker container status
sudo docker ps -a