#!/bin/bash
# Restart Docker containers using docker-compose
sudo docker-compose down
sudo docker-compose up -d
sudo docker ps -a
# Check Docker container status