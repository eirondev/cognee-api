#!/bin/bash

# Deploy script for cognee-api to eva_cognee
# This script copies server.py, .env, and requirements.txt to eva_cognee

REMOTE_HOST="eva_cognee"
REMOTE_USER="root"
REMOTE_DIR="/root/cognee-api"
LOCAL_DIR="/home/steve/DevOps/workspaces/cognee-api"

echo "Deploying cognee-api to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

# Create remote directory if it doesn't exist
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_DIR}"

# Copy files to remote server
echo "Copying files..."
scp ${LOCAL_DIR}/server.py ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${LOCAL_DIR}/.env ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
scp ${LOCAL_DIR}/requirements.txt ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/

echo "Files copied successfully!"
echo ""
echo "To complete the setup on eva_cognee, run:"
echo "  ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "  cd ${REMOTE_DIR}"
echo "  pip install -r requirements.txt"
echo "  python server.py"
