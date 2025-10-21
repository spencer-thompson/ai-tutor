#!/usr/bin/env bash
set -euo pipefail

# Prompt for IP (use root as user)
read -rp "Enter server IP (will use user 'root'): " SERVER_IP
if [[ -z "$SERVER_IP" ]]; then
  echo "No IP entered. Exiting."
  exit 1
fi

# Check dependencies
if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed or not on PATH"
  exit 1
fi
if ! command -v scp >/dev/null 2>&1; then
  echo "scp is not installed or not on PATH"
  exit 1
fi

# Find the most recently created image
IMAGE_LINE=$(docker images --format '{{.CreatedAt}}\t{{.Repository}}:{{.Tag}}\t{{.ID}}' | sort -r | head -n1 || true)
if [[ -z "$IMAGE_LINE" ]]; then
  echo "No docker images found."
  exit 1
fi

IMAGE=$(printf '%s' "$IMAGE_LINE" | cut -f2)
IMAGE_ID=$(printf '%s' "$IMAGE_LINE" | cut -f3)

echo "Latest image: $IMAGE (ID: $IMAGE_ID)"

# Prepare filename (sanitize slashes/colons)
SANITIZED_IMAGE=$(echo "$IMAGE" | tr '/:' '_')
OUTFILE="${SANITIZED_IMAGE}_$(date +%Y%m%d%H%M%S).tar"

echo "Saving image to $OUTFILE..."
docker save -o "$OUTFILE" "$IMAGE"

# SCP to remote server (root)
REMOTE_PATH="/root/$OUTFILE"
echo "Copying $OUTFILE to root@${SERVER_IP}:${REMOTE_PATH} ..."
scp -q "$OUTFILE" "root@${SERVER_IP}:${REMOTE_PATH}"

if [[ $? -eq 0 ]]; then
  echo "File copied successfully to root@${SERVER_IP}:${REMOTE_PATH}"
  read -rp "Remove local file $OUTFILE? [y/N]: " REMOVE_ANSWER
  if [[ "${REMOVE_ANSWER,,}" == "y" ]]; then
    rm -f "$OUTFILE"
    echo "Local file removed."
  else
    echo "Local file retained: $OUTFILE"
  fi
else
  echo "scp failed. Local file retained: $OUTFILE"
  exit 1
fi
