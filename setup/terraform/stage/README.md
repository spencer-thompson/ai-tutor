# Hetzner Terraform skeleton (cx23 Ubuntu)

This folder contains a minimal Terraform skeleton to create a single Hetzner Cloud cx23 Ubuntu server in Helsinki (`hel1`). It's tuned for local use in WSL2 and CI.

Requirements
- Terraform >= 1.5
- Hetzner API token

Quick start (WSL / Linux)

1. Set your Hetzner token. You can either export `HCLOUD_TOKEN` in the shell or create a `.env` file in this directory with `HCLOUD_TOKEN=<your-token>`.

```bash
# Option A: export in shell (temporary for session)
export HCLOUD_TOKEN="<your-token>"

# Option B: copy and edit .env (recommended for WSL local runs)
cp .env.example .env
${EDITOR:-nano} .env
# ensure HCLOUD_TOKEN is set inside .env
```

2. Initialize Terraform and apply (reads the default SSH public key at `~/.ssh/id_ed25519.pub`):

```bash
terraform init
# Then run the helper (it will read HCLOUD_TOKEN from .env if present):
./wsl_apply.sh
```

3. Destroy when done:

```bash
terraform destroy -var "hcloud_token=$HCLOUD_TOKEN"
```

Notes
- The `cloud-init.yaml` is a simple placeholder. It will be uploaded as `user_data`. The SSH public key is read from the path defined in `variables.tf` by default `~/.ssh/id_ed25519.pub`.
- The terraform files are intentionally minimal; they do not include remote state. For production usage, configure a remote backend and secrets management.

Optional helpers
Using existing SSH key
----------------------

If you've already uploaded an SSH key in the Hetzner Cloud console, you can avoid the `SSH key not unique` error by telling Terraform to use that existing key instead of creating a new one.

1. Set `create_ssh_key=false` and provide `existing_ssh_key_id` in your `.env` (or set TF_VAR_existing_ssh_key_id):

```bash
CREATE_SSH_KEY=false
EXISTING_SSH_KEY_ID="123456"
```

2. Then run `./wsl_apply.sh` as usual. Terraform will use the provided key id.

If you need the existing key id, you can find it in the Hetzner Cloud Console under SSH Keys, or list keys using `hcloud` CLI (if installed):

```bash
hcloud ssh-key list
```

- Copy `.env.example` to `.env` and fill values before running the scripts.
- Two helper scripts are provided for WSL in this directory:
	- `wsl_apply.sh` — sources `.env` and runs `terraform init` + `terraform apply -auto-approve`.
	- `wsl_destroy.sh` — sources `.env` and runs `terraform destroy -auto-approve`.

Optional: Create an AWS S3 bucket for environment variables
---------------------------------------------------------

If you'd like Terraform to also create a private AWS S3 bucket to store environment files, enable it by setting `CREATE_ENV_BUCKET=true` in your `.env` (or `-var 'create_env_bucket=true'`). The bucket name will be generated from the `ENV_BUCKET_NAME_PREFIX` plus a short random suffix.

Required AWS credentials
- Set AWS credentials using the standard methods (environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and optional AWS_SESSION_TOKEN), or configure a shared credentials/profile in `~/.aws/credentials`.

Example `.env` entries (optional):

```bash
CREATE_ENV_BUCKET=true
ENV_BUCKET_NAME_PREFIX=aitutor-env
ENV_BUCKET_REGION=us-east-1
```

When enabled, Terraform will create the bucket and output its name as `env_bucket_name` in the outputs.

Quick WSL usage

```bash
# Copy example .env and edit
cp .env.example .env
${EDITOR:-nano} .env
# Then run (WSL):
./wsl_apply.sh
```

Destroy with WSL helper

```bash
./wsl_destroy.sh
```

Static IP note
-- The skeleton supports allocating a floating/static IP (`use_floating_ip` variable). If you prefer the server's primary IP instead of a floating IP, set `USE_FLOATING_IP=false` in your `.env` or edit the Terraform variable.
