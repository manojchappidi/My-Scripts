#!/bin/bash

# Navigate to the ansible-pathflow-app-deploy directory
cd ansible-pathflow-app-deploy || { echo "Directory not found"; exit 1; }

# Make the install_ansible.sh script executable
echo "Making install_ansible.sh executable..."
sudo chmod +x install_ansible.sh

# Run the install_ansible.sh script
echo "Running install_ansible.sh..."
sudo ./install_ansible.sh

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo "Failed to run install_ansible.sh. Please check the logs."
    exit 1
fi

# Run the Ansible playbook
echo "Running the Ansible playbook..."
ansible-playbook deploy_pathflowdx.yml

# Check if the playbook ran successfully
if [ $? -eq 0 ]; then
    echo "Playbook executed successfully. Returning to pathflow directory..."
    # Navigate back to the pathflow directory
    cd ../pathflow || { echo "Directory not found"; exit 1; }

    # Docker login
    echo "Logging into Docker..."
    sudo docker login

    # Run Docker commands
    echo "Building and starting Docker containers..."
    sudo docker-compose up -d --build

    # List Docker containers
    echo "Listing Docker containers..."
    sudo docker ps -a
else
    echo "Playbook execution failed. Please check the logs."
    exit 1
fi
