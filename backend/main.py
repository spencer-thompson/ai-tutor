import os
from contextlib import asynccontextmanager
from logging import info  # @asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = f'mongodb://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("DOMAIN")}'

# --- INIT ---


async def db_lifespan(app: FastAPI):
    # Startup

    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    else:
        info("Connected to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()


app = FastAPI(lifespan=db_lifespan)

# --- ENDPOINTS ---


@app.get("/")
async def read_root():
    return {"Hello", "World"}
