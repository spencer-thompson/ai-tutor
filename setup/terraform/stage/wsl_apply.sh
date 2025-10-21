#!/usr/bin/env bash
set -euo pipefail

# Normalize and load .env if present (fix CRLF from Windows editors)
if [ -f .env ]; then
  if grep -q $'\r' .env; then
    echo ".env contains CRLF line endings — normalizing to LF"
    if command -v dos2unix >/dev/null 2>&1; then
      dos2unix .env
    else
      # sed edit-in-place to remove CR characters
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

masked_len=$(echo -n "$HCLOUD_TOKEN" | wc -c)
echo "Using HCLOUD_TOKEN with length: ${masked_len} (should be 64)"

export TF_VAR_hcloud_token="${HCLOUD_TOKEN}"
export TF_VAR_ssh_public_key_path="${SSH_PUBLIC_KEY_PATH:-$HOME/.ssh/id_ed25519.pub}"
export TF_VAR_instance_name="${INSTANCE_NAME:-aitutor-cx23}"
export TF_VAR_use_floating_ip=${USE_FLOATING_IP:-true}
export TF_VAR_create_ssh_key=${CREATE_SSH_KEY:-true}
export TF_VAR_existing_ssh_key_id="${EXISTING_SSH_KEY_ID:-}"

# Add GitHub Container Registry variables (can be set in .env)
# NOTE: Docker image build/push removed. This script now only provisions resources with Terraform

# If user doesn't want Terraform to upload a new key but didn't provide an existing id,
# try to find a matching key in Hetzner by comparing the public key text via API.
if [ "${CREATE_SSH_KEY:-true}" = "false" ] && [ -z "${EXISTING_SSH_KEY_ID:-}" ]; then
  echo "CREATE_SSH_KEY is false and EXISTING_SSH_KEY_ID not provided — attempting to auto-detect existing SSH key in Hetzner..."
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required for auto-detection. Please install python3 or set EXISTING_SSH_KEY_ID in .env."
  else
    pubkey_path="${SSH_PUBLIC_KEY_PATH:-$HOME/.ssh/id_ed25519.pub}"
    if [ ! -f "${pubkey_path}" ]; then
      echo "Public key file not found at ${pubkey_path}. Please set SSH_PUBLIC_KEY_PATH in .env or provide EXISTING_SSH_KEY_ID."
    else
      pubkey=$(sed 's/\r$//' "${pubkey_path}" | tr -d '\n')
      existing_id=$(curl -s -H "Authorization: Bearer ${HCLOUD_TOKEN}" "https://api.hetzner.cloud/v1/ssh_keys" | python3 -c "import sys,json; data=json.load(sys.stdin); pk='''${pubkey}''';
for k in data.get('ssh_keys',[]):
    if k.get('public_key','').strip() == pk.strip():
        print(k.get('id'))
        sys.exit(0)
sys.exit(1)") || true

      if [ -n "${existing_id}" ]; then
        echo "Found existing SSH key in Hetzner with id ${existing_id}; using that."
        export TF_VAR_existing_ssh_key_id="${existing_id}"
      else
        echo "Could not find a matching SSH key in Hetzner. Please set EXISTING_SSH_KEY_ID in .env or allow Terraform to upload a key."
      fi
    fi
  fi
fi

terraform init
terraform apply -auto-approve

# Docker-related build/push steps intentionally removed per user request.
