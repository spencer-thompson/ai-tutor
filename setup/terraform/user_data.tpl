#!/bin/bash
apt-get update && apt-get install -y docker.io unzip curl docker-compose-v2
 
# Install AWS CLI v2
# The apt package for awscli is often outdated or not available for newer Ubuntu versions.
# Using the official installer ensures the latest version and broader compatibility.
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
rm -rf awscliv2.zip aws

# Verify AWS CLI installation (optional, but good for debugging user_data scripts)
aws --version
# Configure awscli with Hetzner endpoint via env vars or a config file
export AWS_ACCESS_KEY_ID=${s3_access_key}
export AWS_SECRET_ACCESS_KEY=${s3_secret_key}

# Create a directory for the application
mkdir -p /opt/ai-tutor
cd /opt/ai-tutor

# Download the environment file and compose file
aws --endpoint-url https://hel1.your-objectstorage.com s3 cp s3://ai-tutor/env/staging.env ./.env
aws --endpoint-url https://hel1.your-objectstorage.com s3 cp s3://ai-tutor/compose/develop.yaml ./develop.yaml
chmod 600 ./.env

# Download and load the custom-built images
aws --endpoint-url https://hel1.your-objectstorage.com s3 cp s3://ai-tutor/images/ai-tutor-staging.tar.gz .
gzip -dc ai-tutor-staging.tar.gz | docker load
rm ai-tutor-staging.tar.gz

# Set the host port for the application. This ensures Traefik listens on the correct port
# that is exposed by the firewall. We append it to the .env file.
echo "HOST_PORT=8080" >> ./.env

# Run the application using docker compose
# This will pull public images (mongo, traefik) and use the loaded custom images.
docker compose --file develop.yaml up -d
