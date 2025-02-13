#!/bin/bash

# Update system packages
sudo apt update -y
sudo apt upgrade -y

# Install prerequisite packages
sudo apt install -y software-properties-common

# Add Ansible PPA repository and update package list
sudo add-apt-repository --yes --update ppa:ansible/ansible

# Install Ansible
sudo apt install -y ansible

# Verify Ansible installation
ansible --version
