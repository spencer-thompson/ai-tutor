#!/usr/bin/env bash
set -euo pipefail

# Normalize and load .env if present (fix CRLF from Windows editors)
if [ -f .env ]; then
  if grep -q $'\r' .env; then
    echo ".env contains CRLF line endings — normalizing to LF"
    if command -v dos2unix >/dev/null 2>&1; then
      dos2unix .env
    else
      sed -i 's/\r$//' .env
    fi
  fi
  # shellcheck disable=SC1091
  source .env
fi

if [ -z "${HCLOUD_TOKEN:-}" ]; then
  echo "HCLOUD_TOKEN is not set. Please copy .env.example to .env and set HCLOUD_TOKEN."
  exit 1
fi

export TF_VAR_hcloud_token="${HCLOUD_TOKEN}"
export TF_VAR_ssh_public_key_path="${SSH_PUBLIC_KEY_PATH:-$HOME/.ssh/id_ed25519.pub}"
export TF_VAR_instance_name="${INSTANCE_NAME:-aitutor-cx23}"
export TF_VAR_use_floating_ip=${USE_FLOATING_IP:-true}
export TF_VAR_create_ssh_key=${CREATE_SSH_KEY:-true}
export TF_VAR_existing_ssh_key_id="${EXISTING_SSH_KEY_ID:-}"

terraform destroy -auto-approve
