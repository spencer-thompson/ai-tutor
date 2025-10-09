#!/usr/bin/env bash
#
# Local bootstrap for ai-tutor (POSIX)
#
# Usage: ./bootstrap.sh [OPTIONS]
#
# Options:
#   --no-build   Skip building Docker images.
#   --force      Overwrite existing .env.local/.env if present.
#   --auto       Don't prompt; use defaults.
#   --reset      Stop services and delete all associated data volumes.
#   -h, --help   Show this help message.
#

set -euo pipefail

# --- Constants -------------------------------------------------------------
# Uncomment the next line to debug script execution step-by-step:
# set -x

# Paths
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
COMPOSE_FILE="$REPO_ROOT/develop.yaml"
TEMPLATE_ENV="$REPO_ROOT/template.env"
DEV_ENV="$REPO_ROOT/dev.env"
ENV_LOCAL="$REPO_ROOT/.env.local"
ENV_FILE="$REPO_ROOT/.env"

# Script arguments
NO_BUILD=0
FORCE=0
AUTO=0
RESET=0

# --- Logging -----------------------------------------------------------------

# ANSI color codes
C_RESET='\e[0m'
C_RED='\e[0;31m'
C_GREEN='\e[0;32m'
C_YELLOW='\e[0;33m'
C_BLUE='\e[0;34m'

msg() {
  echo -e "${C_BLUE}[bootstrap]${C_RESET} $1"
}

msg_ok() {
  echo -e "${C_GREEN}[bootstrap]${C_RESET} $1"
}

msg_warn() {
  echo -e "${C_YELLOW}[bootstrap] [WARNING]${C_RESET} $1"
}

msg_error() {
  echo -e "${C_RED}[bootstrap] [ERROR]${C_RESET} $1" >&2
  exit 1
}

# --- Utility Functions -------------------------------------------------------

check_command() {
  command -v "$1" >/dev/null 2>&1 || msg_error "Required command '$1' not found. Please install it and try again."
}

get_docker_compose_cmd() {
  if command -v "docker-compose" >/dev/null 2>&1;
  then
    echo "docker-compose"
  elif docker compose version >/dev/null 2>&1;
  then
    echo "docker compose"
  else
    msg_error "Neither 'docker-compose' nor 'docker compose' were found. Please install one of them."
  fi
}

# --- Core Functions ----------------------------------------------------------

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --no-build) NO_BUILD=1; shift ;;
      --force) FORCE=1; shift ;;
      --auto) AUTO=1; shift ;;
      --reset) RESET=1; shift ;;
      -h|--help) 
        # Using sed to extract the usage and options from the script's own comments.
        sed -n 's/^# //p' "$0" | sed -n '/(Usage)/,/(Show this help message)/p'
        exit 0
        ;; 
      *) 
        msg_error "Unknown option: $1"
        ;;
    esac
  done
}

setup_environment() {
  msg "Setting up environment..."

  if [[ $FORCE -eq 1 ]]; then
    msg "--force set: will overwrite env files if present"
  fi

  # Determine which env file to use, prioritizing .env.local
  if [[ $FORCE -eq 0 && -f "$ENV_LOCAL" ]]; then
    msg "Found existing env file at '.env.local'. Using it."
    CHOSEN_ENV_FILE="$ENV_LOCAL"
  elif [[ $FORCE -eq 0 && -f "$ENV_FILE" ]]; then
    msg "Found existing env file at '.env'. Using it."
    CHOSEN_ENV_FILE="$ENV_FILE"
  else
    # No .env file found, or --force was used. Create .env.local.
    local source_file=""
    local prompt_msg=""
    if [[ -f "$DEV_ENV" ]]; then
      source_file="$DEV_ENV"
      msg "Creating .env.local from dev.env"
      prompt_msg="You may need to add secrets (like OPENAI_API_KEY) to .env.local. Open it now? (y/N) "
    else
      source_file="$TEMPLATE_ENV"
      msg "Creating .env.local from template.env"
      prompt_msg="Please fill in the secrets in .env.local before continuing. Open it now? (y/N) "
    fi

    cp "$source_file" "$ENV_LOCAL"
    msg_ok "Created .env.local"
    CHOSEN_ENV_FILE="$ENV_LOCAL"

    if [[ $AUTO -eq 0 ]]; then
      read -p "$prompt_msg" yn
      if [[ "$yn" =~ ^[Yy]$ ]]; then
        ${EDITOR:-vi} "$ENV_LOCAL"
      fi
    fi
  fi

  if [[ -z "$CHOSEN_ENV_FILE" ]]; then
    msg_error "Could not find or create an environment file (.env.local or .env)."
  fi

  msg "Using environment file: $CHOSEN_ENV_FILE"
  
  # Validate required environment variables
  msg "Validating required environment variables..."
  check_env_var "MONGO_ROOT_USERNAME"
  check_env_var "MONGO_ROOT_PASSWORD"
  check_env_var "MONGO_DATABASE"
  check_env_var "MONGO_APP_USERNAME"
  check_env_var "MONGO_APP_PASSWORD"
  if ! (grep -q -E "^BACKEND_API_KEY=" "$CHOSEN_ENV_FILE" || grep -q -E "^AITUTOR_API_KEY=" "$CHOSEN_ENV_FILE"); then
    msg_error "Required API key variable is not defined in '$CHOSEN_ENV_FILE'. Please add either 'BACKEND_API_KEY' or 'AITUTOR_API_KEY'."
  fi
  msg_ok "Environment variable validation complete."
}

check_env_var() {
  local var_name=$1
  if ! grep -q -E "^${var_name}=" "$CHOSEN_ENV_FILE"; then
    msg_error "Required variable '${var_name}' is not defined in '$CHOSEN_ENV_FILE'."
  fi
}

get_env_value() {
  local var_name=$1
  grep -E "^${var_name}=" "$CHOSEN_ENV_FILE" | head -n 1 | cut -d'=' -f2- | sed 's/ #.*//' | sed 's/^[ 	]*//;s/[ 	]*$//' | sed 's/$//'
}

check_prerequisites() {
  msg "Checking prerequisites..."
  check_command "docker"
  check_command "curl"
  DOCKER_COMPOSE_CMD=$(get_docker_compose_cmd)
  msg_ok "Prerequisites met."
}

reset_environment() {
  msg "Resetting development environment..."
  msg "This will stop all services and permanently delete the database volume."
  if [[ $AUTO -eq 0 ]]; then
    read -p "Are you sure you want to continue? (y/N) " yn
    if [[ ! "$yn" =~ ^[Yy]$ ]]; then
      msg "Aborting."
      exit 0
    fi
  fi

  local compose_cmd=$(get_docker_compose_cmd)
  $compose_cmd -f "$COMPOSE_FILE" down -v
  msg_ok "Environment has been reset."
  exit 0
}

run_docker_compose() {
  local compose_args=("--env-file" "$CHOSEN_ENV_FILE")
  
  if [[ $NO_BUILD -eq 0 ]]; then
    msg "Building Docker images..."
    $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" "${compose_args[@]}" build
    msg_ok "Images built successfully."
  else
    msg "--no-build set: skipping image build."
  fi

  msg "Starting development stack..."
  msg "MongoDB will be initialized automatically on first run. Check '$DOCKER_COMPOSE_CMD logs mongo'."
  $DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" "${compose_args[@]}" up -d
}

wait_for_services() {
  local domain=$(get_env_value "DOMAIN")
  local host_port=$(get_env_value "HOST_PORT")
  local host_port_effective="${host_port:-80}"
  
  local user_facing_url="http://${domain:-localhost}"
  if [[ "$host_port_effective" != "80" && "$host_port_effective" != "443" ]]; then
    user_facing_url="${user_facing_url}:${host_port_effective}"
  fi

  msg "Waiting for Streamlit to become available (this may take a minute)..."
  
  local streamlit_ready=0
  # Timeout after 20 seconds (10 checks * 2s sleep)
  for i in {1..10}; do
    if curl -fs "$user_facing_url" >/dev/null 2>&1; then
      streamlit_ready=1
      break
    fi
    echo -ne "[bootstrap] Waiting for Streamlit at $user_facing_url...\r"
    sleep 2
  done

  if [[ "$streamlit_ready" -eq 1 ]]; then
    msg_ok "Streamlit is available."
  else
    msg_warn "Timeout: Streamlit did not become available."
    msg_warn "Check logs with: $DOCKER_COMPOSE_CMD -f \"$COMPOSE_FILE\" logs streamlit"
  fi
}

print_summary() {
  local domain=$(get_env_value "DOMAIN")
  local host_port=$(get_env_value "HOST_PORT")
  local host_port_effective="${host_port:-80}"
  
  local user_facing_url="http://${domain:-localhost}"
  if [[ "$host_port_effective" != "80" && "$host_port_effective" != "443" ]]; then
    user_facing_url="${user_facing_url}:${host_port_effective}"
  fi

  cat <<EOF

${C_GREEN}Bootstrap finished.${C_RESET}

${C_YELLOW}Access your services:${C_RESET}
- Streamlit (Main App): ${user_facing_url}
- Mongo Express (DB GUI): ${user_facing_url}/mongo-express

${C_YELLOW}Next steps:${C_RESET}
- Tail logs: ${DOCKER_COMPOSE_CMD} -f ${COMPOSE_FILE} logs -f
- Stop stack: ${DOCKER_COMPOSE_CMD} -f ${COMPOSE_FILE} down
EOF
}

# --- Main Execution ----------------------------------------------------------

main() {
  parse_args "$@"
  
  if [[ $RESET -eq 1 ]]; then
    reset_environment
  fi
  
  check_prerequisites
  setup_environment
  run_docker_compose
  wait_for_services
  print_summary
}

main "$@"