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
#   --push       Build, tag, and push images to object storage.
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
PUSH=0

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
      --push) PUSH=1; shift ;;
      -h|--help) 
        # Using sed to extract the usage and options from the script's own comments.
        sed -n 's/^# //p' "$0" | sed -n '/Usage:/,/(Show this help message)/p'
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
  check_env_var "MONGO_USERNAME"
  check_env_var "MONGO_PASSWORD"
  check_env_var "MONGO_DATABASE"
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
  # 1. Grep for the line starting with the variable name.
  # 2. Use cut to get everything after the first '='.
  # 3. Use sed to remove any trailing comments.
  # 4. Use xargs to trim leading/trailing whitespace and handle special characters robustly.
  #    This avoids issues with values containing slashes, etc.
  # 5. The final sed command removes potential carriage returns from Windows-style line endings.
  grep -E "^${var_name}=" "$CHOSEN_ENV_FILE" | head -n 1 | cut -d'=' -f2- | sed 's/[[:space:]]*#.*$//' | xargs | sed 's/\r$//'
}

check_prerequisites() {
  msg "Checking prerequisites..."
  check_command "docker"
  if [[ $PUSH -eq 1 ]]; then
    check_command "aws"
    msg_ok "AWS CLI found."
  else
    check_command "curl"
  fi
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
  
  # When pushing, we always want to build.
  if [[ $PUSH -eq 1 ]]; then
    NO_BUILD=0
  fi
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

push_images_to_bucket() {
  msg "Starting image push process..."
  local s3_endpoint=$(get_env_value "S3_ENDPOINT_URL")
  local s3_bucket=$(get_env_value "S3_BUCKET")
  local image_tag=$(get_env_value "IMAGE_TAG")

  if [[ -z "$s3_endpoint" || -z "$s3_bucket" || -z "$image_tag" ]]; then
    msg_error "S3_ENDPOINT_URL, S3_BUCKET, and IMAGE_TAG must be defined in $CHOSEN_ENV_FILE for --push to work."
  fi

  # Ensure images are built
  # When pushing, we always want to build, and run_docker_compose handles the build logic.
  # We call it here to ensure images are available for saving.
  NO_BUILD=0 run_docker_compose # Temporarily override NO_BUILD for this call if it was set

  # These are the services with a 'build' directive in develop.yaml
  local services_to_push=("fastapi" "python" "streamlit")
  local all_tagged_images=()

  # Reliably get the project name. Docker Compose uses the directory name by default.
  # We can find it by inspecting the name of a running container for one of our services.
  # The container name is typically <project_name>-<service_name>-<index>.
  # Fallback to directory name if no container is running or label not found.
  local project_name=$($DOCKER_COMPOSE_CMD -f "$COMPOSE_FILE" ps -q fastapi | xargs docker inspect --format '{{ index .Config.Labels "com.docker.compose.project" }}' 2>/dev/null || basename "$REPO_ROOT")
  if [[ -z "$project_name" ]]; then
    msg_error "Could not determine Docker Compose project name. Ensure services are running or define PROJECT_NAME in your .env file."
  fi

  for service in "${services_to_push[@]}"; do
    local image_name="${project_name}-${service}"
    local tagged_image_name="${image_name}:${image_tag}"
    all_tagged_images+=("$tagged_image_name")
    msg "Collected image for combined tarball: $tagged_image_name"
  done

  local combined_tarball_name="ai-tutor-staging.tar.gz" # Consistent with user_data.tpl and plan.md

  msg "Saving all collected images to a single tarball: $combined_tarball_name..."
  docker save "${all_tagged_images[@]}" | gzip > "$combined_tarball_name"

  msg "Uploading $combined_tarball_name to s3://${s3_bucket}/images/ ..."
  aws --endpoint-url "$s3_endpoint" s3 cp "$combined_tarball_name" "s3://${s3_bucket}/images/${combined_tarball_name}"

  if [[ $? -eq 0 ]]; then
    msg_ok "Successfully uploaded ${combined_tarball_name}."
    rm "$combined_tarball_name" # Clean up the local tarball after successful upload
  else
    msg_error "Failed to upload ${combined_tarball_name}."
  fi

  msg "Uploading compose file to s3://${s3_bucket}/compose/ ..."
  aws --endpoint-url "$s3_endpoint" s3 cp "$COMPOSE_FILE" "s3://${s3_bucket}/compose/develop.yaml"
  if [[ $? -eq 0 ]]; then
    msg_ok "Successfully uploaded compose file."
  else
    msg_error "Failed to upload compose file."
  fi
}

# wait_for_services() {
#   local domain=$(get_env_value "DOMAIN")
#   local host_port=$(get_env_value "HOST_PORT")
#   local host_port_effective="${host_port:-80}"
  
#   local user_facing_url="http://${domain:-localhost}"
#   if [[ "$host_port_effective" != "80" && "$host_port_effective" != "443" ]]; then
#     user_facing_url="${user_facing_url}:${host_port_effective}"
#   fi

#   msg "Waiting for Streamlit to become available (this may take a minute)..."
  
#   local streamlit_ready=0
#   # Timeout after 20 seconds (10 checks * 2s sleep)
#   for i in {1..10}; do
#     if curl -fs "$user_facing_url" >/dev/null 2>&1; then
#       streamlit_ready=1
#       break
#     fi
#     echo -ne "[bootstrap] Waiting for Streamlit at $user_facing_url...\r"
#     sleep 2
#   done

#   if [[ "$streamlit_ready" -eq 1 ]]; then
#     msg_ok "Streamlit is available."
#   else
#     msg_warn "Timeout: Streamlit did not become available."
#     msg_warn "Check logs with: $DOCKER_COMPOSE_CMD -f \"$COMPOSE_FILE\" logs streamlit"
#   fi
# }

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
  
  if [[ $PUSH -eq 1 ]]; then
    check_prerequisites
    setup_environment
    push_images_to_bucket
  else
  check_prerequisites
  setup_environment
  run_docker_compose
#   wait_for_services
  print_summary
  fi
}

main "$@"