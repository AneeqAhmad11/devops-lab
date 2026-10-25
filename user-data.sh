#!/bin/bash
# EC2 User Data for the Launch Template (runs once at first boot, as root)
# EDIT the GitHub URL below before pasting.
apt-get update -y
curl -fsSL https://get.docker.com | sh
apt-get install -y git
git clone https://github.com/AneeqAhmad11/devops-lab.git /opt/app
cd /opt/app
docker compose up -d --build
