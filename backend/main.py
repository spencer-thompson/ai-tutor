"""
FastAPI backend for the AI Tutor (webapp and mobile)

Reference: https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520

THOUGHTS:
- This is going to be the "brain" of the whole project, where everything connects together
  that being said we need to create a couple end points
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

# --- V1 ENDPOINTS --- #

# NOTE: we will put all end points for now under the subdirectory `v1`
# for example:
# https://api.aitutor.live/v1/login

# TODO: Setup authorization
# I literally have no idea how to do this


@app.get("/")  # this is a test endpoint just to see if it working
async def read_root():
    return {"Hello": "World"}


@app.get("/test_user")
async def test_user():
    return {
        "Hello": "World",
    }


# NOTE: we need to define the data that the endpoint takes, just like a function call
# we need to figure out the required and not required parameters for each

# TODO: | /v1/ingest
# something like this to send data from extension

# TODO: | /v1/login
#       | /v1/logout
# just an endpoint(s) to login/logout

# TODO: | /v1/message
# get a message from the tutor aka send a message to the tutor and get a response back
