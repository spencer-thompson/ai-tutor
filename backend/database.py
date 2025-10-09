import os
import sys
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# WARNING: This is a standalone utility script for testing database connections.
# Do NOT import this module into the main FastAPI application, because it
# configures the root logger with `logging.basicConfig()` which can interfere
# with centralized logging configured by the application. If you need to call
# code here from other modules, import functions and ensure the root logging
# configuration is performed by the application entrypoint instead.
if __name__ == "__main__":
    # Configure logging only when the script is executed directly.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [DB] - %(message)s',
        stream=sys.stdout,
    )

# --- Database Configuration ---
# Read credentials and configuration from environment variables
MONGO_USERNAME = os.getenv("MONGO_APP_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_APP_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE", "admin")

# --- Connection Setup ---
client = None
db = None

try:
    # Validate that all necessary environment variables are set
    if not all([MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_DATABASE]):
        raise ValueError("One or more MongoDB environment variables are not set.")

    # Construct the full connection URI
    MONGO_URI = (
        f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/"
        f"{MONGO_DATABASE}?authSource={MONGO_AUTH_SOURCE}"
    )

    # Create a redacted URI for safe logging to avoid exposing passwords
    REDACTED_URI = (
        f"mongodb://{MONGO_USERNAME}:<REDACTED>@{MONGO_HOST}:27017/"
        f"{MONGO_DATABASE}?authSource={MONGO_AUTH_SOURCE}"
    )

    logging.info(f"Attempting to connect to MongoDB...")
    logging.info(f"Connection String: {REDACTED_URI}")

    # Instantiate the client and force a connection test
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Verifies connection and authentication

    logging.info("MongoDB connection successful and authenticated.")
    db = client[MONGO_DATABASE]

except (ConnectionFailure, OperationFailure, ValueError) as e:
    logging.error(f"DATABASE CONNECTION FAILED: {e}")
    # Exit the application since it cannot function without a database
    sys.exit(1)