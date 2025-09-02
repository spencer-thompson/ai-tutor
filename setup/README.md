# Local Bootstrap Script

This folder contains helper scripts that prepare a local development environment for the ai-tutor project.

## File

- `bootstrap.sh` — A POSIX shell script for setting up the environment.

## Usage

```sh
./setup/bootstrap.sh [OPTIONS]
```

### Options

-   `--no-build`: Skips building Docker images and uses existing ones.
-   `--force`: Overwrites an existing `.env.local` or `.env` file.
-   `--auto`: Runs non-interactively, using defaults and suppressing prompts.
-   `--reset`: Stops all services and permanently deletes all associated data volumes, including the database. **This is a destructive action.**
-   `-h`, `--help`: Displays the help message.

## What the script does

1.  **Prerequisite Checks**: Ensures required commands like `docker`, `docker compose`, and `curl` are installed.
2.  **Port Check**: Verifies that the required host port (defined by `HOST_PORT` in your `.env` file) is not already in use.
3.  **Environment Setup**: Creates a `.env.local` file for local configuration if one doesn't exist. It will use `dev.env` as a template if it exists, otherwise it falls back to `template.env`.
4.  **Build Images**: Builds the necessary Docker images using `develop.yaml` (this step is skipped if `--no-build` is provided).
5.  **Start Services**: Starts the full development stack (Streamlit, Backend, Mongo, etc.) in detached mode using `docker compose`. The MongoDB service will automatically initialize the database on its first run.
6.  **Health Check**: Waits and checks to see when the Streamlit service becomes available.

## Notes

- The script is idempotent and safe to re-run. Use `--force` to regenerate your `.env.local` file.
- For non-interactive usage (e.g., in other scripts), use `--auto` to accept defaults and prevent prompts.

## Next steps

- A CI/CD pipeline could use this script for integration testing, for example: `bootstrap.sh --auto --no-build`.
