"""
FastAPI backend for the AI Tutor (webapp and mobile)

Reference: https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520
"""

import os
from contextlib import asynccontextmanager
from logging import info  # @asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = f'mongodb://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("DOMAIN")}'

# --- INIT ---


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup

    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.mongodb = app.mongodb_client.get_default_database()  # can use `get_database()` method
    ping_response = await app.mongodb.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    else:
        info("Connected to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()


# app = FastAPI(lifespan=db_lifespan)
app = FastAPI()

# --- ENDPOINTS ---


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test_user")
async def test_user():
    return {
        "Hello": "World",
    }
