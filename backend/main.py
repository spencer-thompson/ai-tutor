"""
FastAPI backend for the AI Tutor (webapp and mobile)

Reference: https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520

THOUGHTS:
- This is going to be the "brain" of the whole project, where everything connects together
  that being said we need to create a couple end points
"""

import os
from contextlib import asynccontextmanager
from logging import info
from typing import List

from fastapi import FastAPI
from fastapi.responses import StreamingResponse  # TODO: add streaming response
from models import Message
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI

CONNECTION_STRING = f'mongodb://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@mongo'
CHAT_MODEL = os.getenv("CHAT_MODEL")

# TODO: Add API keys properly,
# this will fix issue #7


# --- INIT ---
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup

    # setup mongo
    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.mongodb = app.mongodb_client.get_database("aitutor")
    ping_response = await app.mongodb.command("ping")

    # Setup OpenAI
    app.openai = AsyncOpenAI()

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    else:
        info("Connected to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()


app = FastAPI(lifespan=db_lifespan)
# app = FastAPI()

# --- V1 ENDPOINTS --- #

# NOTE: we will put all end points for now under the subdirectory `v1`
# for example:
# https://api.aitutor.live/v1/login


@app.get("/")  # this is a test endpoint just to see if it working
async def read_root():
    return {"Hello": "World"}


@app.get("/test_user")
async def test_user():
    users = await app.mongodb["users"].find().to_list(None)
    # Convert ObjectId to string
    for user in users:
        # TODO: implement modeling to avoid this
        # This is just a workaround for now
        user["_id"] = str(user["_id"])
    return users


@app.post("/v1/chat")
async def chat(messages: List[Message]):
    completion = await app.openai.chat.completions.create(
        messages=messages,
        model=CHAT_MODEL,
    )
    return completion.choices[0].message


# NOTE: we need to define the data that the endpoint takes, just like a function call
# we need to figure out the required and not required parameters for each

# TODO: | /v1/ingest
# something like this to send data from extension

# TODO: | /v1/login
#       | /v1/logout
# just an endpoint(s) to login/logout

# TODO: | /v1/message
# get a message from the tutor aka send a message to the tutor and get a response back
