#!/usr/bin/env bash
# Local bootstrap for ai-tutor (POSIX)
# Usage: ./bootstrap.sh [--no-build] [--force] [--auto]
set -euo pipefail

# Uncomment the next line to debug script execution step-by-step:
set -x

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
COMPOSE_FILE="$REPO_ROOT/develop.yaml"
TEMPLATE_ENV="$REPO_ROOT/template.env"
DEV_ENV="$REPO_ROOT/dev.env"
ENV_LOCAL="$REPO_ROOT/.env.local"
ENV_FILE="$REPO_ROOT/.env"
CHOSEN_ENV_FILE=""

NO_BUILD=0
FORCE=0
AUTO=0
RESET=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-build) NO_BUILD=1; shift ;;
    --force) FORCE=1; shift ;;
    --auto) AUTO=1; shift ;;
    --reset) RESET=1; shift ;;
    -h|--help)
      cat <<EOF
Usage: bootstrap.sh [OPTIONS]

Options:
  --no-build   Skip building Docker images.
  --force      Overwrite existing .env.local/.env if present.
  --auto       Don't prompt; use defaults (copy dev.env if present, else template.env).
  --reset      Stop services and delete all associated data volumes.
EOF
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

check_command() {
  command -v "$1" >/dev/null 2>&1 || { echo "Required command '$1' not found. Aborting."; exit 1; }
}

check_env_var() {
  local var_name=$1
  local file=$2
  if ! grep -q -E "^${var_name}=" "$file"; then
    echo "[bootstrap] [ERROR] Required variable '${var_name}' is not defined in '$file'."
    echo "[bootstrap] Please add it and try again. You may need to copy it from 'template.env' or 'dev.env'."
    echo "[bootstrap] [DEBUG] Exiting due to missing env var: $var_name"
    exit 1
  fi
}

get_env_value() {
  local var_name=$1
  local file=$2
  grep -E "^${var_name}=" "$file" | head -n 1 | cut -d'=' -f2- | sed 's/ #.*//' | sed 's/^[ \t]*//;s/[ \t]*$//' | sed 's/\r$//'
}

check_port() {
  local port=$1
  local err_msg="[bootstrap] [ERROR] Port $port is already in use. Please stop the conflicting service."
  local hint_msg="[bootstrap] Hint: If the process is 'vmmem' or similar, a service inside WSL might be the cause."

  if command -v lsof >/dev/null 2>&1; then
    if lsof -i :"$port" -sTCP:LISTEN -t >/dev/null; then
      echo "$err_msg"
      echo "[bootstrap] The following process is using port $port:"
      lsof -i :"$port" -sTCP:LISTEN
      echo "$hint_msg"
      exit 1
    fi
  elif command -v ss >/dev/null 2>&1; then
    if ss -lnt | grep -q ":$port "; then
      echo "$err_msg"; echo "$hint_msg"; exit 1
    fi
  elif command -v netstat >/dev/null 2>&1; then
    if netstat -lnt | grep -q ":$port "; then
      echo "$err_msg"; echo "$hint_msg"; exit 1
    fi
  else
    echo "********************************************************************************"
    echo "[bootstrap] [CRITICAL WARNING] Cannot check for port conflicts."
    echo "[bootstrap] Required tools ('lsof', 'ss', or 'netstat') not found."
    echo "[bootstrap] If startup fails, it may be because port $port is already in use."
    echo "********************************************************************************"
  fi
}

echo "[bootstrap] Starting local bootstrap"

if [[ $RESET -eq 1 ]]; then
  echo "[bootstrap] Resetting development environment..."
  echo "[bootstrap] This will stop all services and permanently delete the database volume."
  if [[ $AUTO -eq 0 ]]; then
    read -p "Are you sure you want to continue? (y/N) " yn
    if [[ ! "$yn" =~ ^[Yy]$ ]]; then
      echo "Aborting."
      exit 0
    fi
  fi

  if docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" down -v
  else
    docker-compose -f "$COMPOSE_FILE" down -v
  fi
  echo "[bootstrap] Environment has been reset."
  exit 0
fi

# Prereqs
check_command docker
if ! (docker compose version >/dev/null 2>&1 || docker-compose --version >/dev/null 2>&1); then
  echo "Required command 'docker compose' or 'docker-compose' not found. Aborting." >&2
  exit 1
fi
check_command curl || echo "warning: curl not found; healthchecks will be skipped"

# Create env file if needed
if [[ $FORCE -eq 1 ]]; then
  echo "[bootstrap] --force set: will overwrite env files if present"
fi

# Determine which env file to use, prioritizing .env.local
if [[ $FORCE -eq 0 && -f "$ENV_LOCAL" ]]; then
  echo "[bootstrap] Found existing env file at '.env.local'. Using it."
  CHOSEN_ENV_FILE="$ENV_LOCAL"
elif [[ $FORCE -eq 0 && -f "$ENV_FILE" ]]; then
  # Note: docker-compose automatically picks up .env, but we specify it for consistency
  # and to ensure it's used even if the script is run from a different directory.
  echo "[bootstrap] Found existing env file at '.env'. Using it."
  CHOSEN_ENV_FILE="$ENV_FILE"
else
  # No .env file found, or --force was used. Create .env.local.
  # Prefer dev.env if it exists, otherwise fall back to the template.
  SOURCE_FILE=""
  PROMPT_MSG=""
  if [[ -f "$DEV_ENV" ]]; then
    SOURCE_FILE="$DEV_ENV"
    echo "[bootstrap] Creating .env.local from dev.env"
    PROMPT_MSG="You may need to add secrets (like OPENAI_API_KEY) to .env.local. Open it now? (y/N) "
  else
    SOURCE_FILE="$TEMPLATE_ENV"
    echo "[bootstrap] Creating .env.local from template.env"
    PROMPT_MSG="Please fill in the secrets in .env.local before continuing. Open it now? (y/N) "
  fi

  cp "$SOURCE_FILE" "$ENV_LOCAL"
  echo "[bootstrap] Created .env.local"
  CHOSEN_ENV_FILE="$ENV_LOCAL"

  if [[ $AUTO -eq 0 ]]; then
    read -p "$PROMPT_MSG" yn
    if [[ "$yn" =~ ^[Yy]$ ]]; then
      ${EDITOR:-vi} "$ENV_LOCAL"
    fi
  fi
fi

if [[ -z "$CHOSEN_ENV_FILE" ]]; then
  echo "[bootstrap] [CRITICAL] Could not find or create an environment file (.env.local or .env). Aborting." >&2
  exit 1
fi

echo "[bootstrap] Using environment file: $CHOSEN_ENV_FILE"

echo "[bootstrap] Validating required environment variables..."
check_env_var "MONGO_ROOT_USERNAME" "$CHOSEN_ENV_FILE"
check_env_var "MONGO_ROOT_PASSWORD" "$CHOSEN_ENV_FILE"
check_env_var "MONGO_DATABASE" "$CHOSEN_ENV_FILE"
check_env_var "MONGO_APP_USERNAME" "$CHOSEN_ENV_FILE"
check_env_var "MONGO_APP_PASSWORD" "$CHOSEN_ENV_FILE"
# Check for either API key variable to exist for compatibility.
if ! (grep -q -E "^BACKEND_API_KEY=" "$CHOSEN_ENV_FILE" || grep -q -E "^AITUTOR_API_KEY=" "$CHOSEN_ENV_FILE"); then
  echo "[bootstrap] [ERROR] Required API key variable is not defined in '$CHOSEN_ENV_FILE'." >&2
  echo "[bootstrap] Please add either 'BACKEND_API_KEY' or 'AITUTOR_API_KEY' and try again." >&2
  echo "[bootstrap] [DEBUG] Exiting due to missing API key variable"
  exit 1
fi

echo "[bootstrap] Environment variable validation complete."

# Debug: Show which env file and first few lines (not secrets)
echo "[bootstrap] DEBUG: Using env file $CHOSEN_ENV_FILE"
head -n 10 "$CHOSEN_ENV_FILE" | grep -v -i 'key\|password' || true

compose_args=(--env-file "$CHOSEN_ENV_FILE")

# Read DOMAIN and HOST_PORT from the chosen env file and sanitize them
DOMAIN=$(get_env_value "DOMAIN" "$CHOSEN_ENV_FILE")
HOST_PORT=$(get_env_value "HOST_PORT" "$CHOSEN_ENV_FILE")

echo "[bootstrap] DEBUG: DOMAIN='$DOMAIN' (from $CHOSEN_ENV_FILE)"
echo "[bootstrap] DEBUG: HOST_PORT='$HOST_PORT'"

# Warn if DOMAIN looks like a typo or is empty
if [[ -z "$DOMAIN" ]]; then
  echo "[bootstrap] [WARNING] DOMAIN variable is empty. Defaulting to 'localhost'."
  DOMAIN="localhost"
elif [[ "$DOMAIN" =~ localhos$ ]]; then
  echo "[bootstrap] [WARNING] DOMAIN variable ends with 'localhos'. Did you mean 'localhost'?"
fi

# Proactively check if the domain is likely configured in the hosts file
if [[ -n "$DOMAIN" && "$DOMAIN" != "localhost" ]]; then
  # Check for both the base domain and the api subdomain used by the extension
  for d in "$DOMAIN" "api.$DOMAIN"; do
    # Use getent for a more robust check if available, otherwise fallback to grep
    if command -v getent >/dev/null 2>&1 && ! getent hosts "$d" | awk '{print $1}' | grep -q "127\.0\.0\.1"; then
        echo "[bootstrap] [WARNING] Domain '$d' may not be configured correctly in your hosts file." >&2
        echo "[bootstrap] [WARNING] Please ensure '127.0.0.1 $d' is present in your hosts file to ensure proper communication." >&2
    fi
  done
fi

# Check if the target port is free before starting services
HOST_PORT_EFFECTIVE="${HOST_PORT:-80}"
echo "[bootstrap] Verifying that port ${HOST_PORT_EFFECTIVE} is available..."
check_port "${HOST_PORT_EFFECTIVE}"

if [[ $NO_BUILD -eq 0 ]]; then
  echo "[bootstrap] Building images"
  # Use docker compose v2 if available
  if docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" "${compose_args[@]}" build
  else
    docker-compose -f "$COMPOSE_FILE" "${compose_args[@]}" build
  fi
else
  echo "[bootstrap] --no-build set: skipping image build"
fi

echo "[bootstrap] Starting development stack"
echo "[bootstrap] MongoDB will be initialized automatically on first run. Check 'docker compose logs mongo'."
if docker compose version >/dev/null 2>&1; then
  docker compose -f "$COMPOSE_FILE" "${compose_args[@]}" up -d
else
  docker-compose -f "$COMPOSE_FILE" "${compose_args[@]}" up -d
fi

echo "[bootstrap] Waiting for Streamlit to become available (this may take a minute)..."

USER_FACING_URL="http://${DOMAIN:-localhost}"
if [[ "$HOST_PORT_EFFECTIVE" != "80" && "$HOST_PORT_EFFECTIVE" != "443" ]]; then
  USER_FACING_URL="${USER_FACING_URL}:${HOST_PORT_EFFECTIVE}"
fi

streamlit_ready=0
# Timeout after 20 seconds (10 checks * 2s sleep)
for i in {1..10}; do
  # Use curl to check if the service is responding without an error.
  # -f: fail on server errors (4xx, 5xx), -s: silent.
  if command -v curl >/dev/null 2>&1 && curl -fs "$USER_FACING_URL" >/dev/null 2>&1; then
    streamlit_ready=1
    break
  fi
  echo -ne "[bootstrap] Waiting for Streamlit at $USER_FACING_URL...\r"
  sleep 2
done

if [[ "$streamlit_ready" -eq 1 ]]; then
  echo -e "\r\033[K[bootstrap] Streamlit is available at: $USER_FACING_URL"
  echo "[bootstrap] Mongo Express is available at: ${USER_FACING_URL}/mongo-express"
else
  echo -e "\r\033[K[bootstrap] Timeout: Streamlit did not become available." >&2
  echo "[bootstrap] Check logs with: docker compose -f \"$COMPOSE_FILE\" logs streamlit" >&2
fi

cat <<EOF

Bootstrap finished.
- Logs: use 'docker compose -f develop.yaml logs -f' to tail logs.
- Stop the stack with: docker compose -f develop.yaml down
EOF

exit 0
