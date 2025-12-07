import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os


@pytest_asyncio.fixture(scope="function")
async def test_db():
    """
    Provides a clean test database for each test function.
    Connects to the MongoDB instance defined by environment variables,
    creates a test database, yields it to the test, and then drops it.
    """
    mongo_user = os.getenv("MONGO_USERNAME")
    mongo_pass = os.getenv("MONGO_PASSWORD")
    mongo_host = "mongo"  # The service name in docker-compose
    db_name = "test_ai_tutor"

    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017"
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]

    yield db

    # Teardown: drop the test database after the test function completes
    await client.drop_database(db_name)
    client.close()