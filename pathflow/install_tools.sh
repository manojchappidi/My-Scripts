#!/bin/bash

# Run the Docker installation script
echo "Running Docker installation script..."
./install_docker.sh

# Update the package list
echo "Updating package list..."
sudo apt-get update

# Install Python 3, Nginx, and Certbot
echo "Installing Python 3, Nginx, and Certbot..."
sudo apt-get install -y python3 nginx certbot

# Check the installation status
echo "Checking installed versions..."
python3 --version
nginx -v
certbot --version

echo "Installation complete."
