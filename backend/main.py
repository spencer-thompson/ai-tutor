"""
FastAPI backend for the AI Tutor (webapp and mobile)

Reference: https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520

THOUGHTS:
- This is going to be the "brain" of the whole project, where everything connects together
  that being said we need to create a couple end points
"""

import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from logging import info
from typing import List

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from models import CanvasData, Message, Token, User
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI

BACKEND_API_KEY_NAME = os.getenv("BACKEND_API_KEY_NAME")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
CONNECTION_STRING = f'mongodb://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@mongo/?authSource=admin'
CHAT_MODEL = os.getenv("CHAT_MODEL")
SYSTEM_MESSAGE = [
    {
        "role": "system",
        "content": """
    You are an AI Tutor for Utah Valley University with a bright and excited attitude and tone.
    Respond in a concise and effictive manner. Format your response in github flavored markdown.
    """,
    }
]
# Query params can be read by extension


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://uvu.instructure.com",
        "http://localhost:8080",
        "http://localhost:5555",
    ],  # List the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
header_scheme = APIKeyHeader(name=BACKEND_API_KEY_NAME)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def check_api_key(api_key: str = Security(header_scheme)) -> bool:
    document = await app.mongodb["keys"].find_one({api_key: {"$exists": True}})
    if document:
        return [v for k, v in document.items() if k not in {"_id"}][0]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=1)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id = payload.get("sub")
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await app.mongodb["users"].find_one({"canvas_id": id, "institution": uni})
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # return {
    #     "first_name": user.get("first_name"),
    #     "last_name": user.get("last_name"),
    #     "avatar_url": user.get("avatar_url"),
    #     "courses": user.get("courses"),
    # }


# --- V1 ENDPOINTS --- #

# NOTE: we will put all end points for now under the subdirectory `v1`
# for example:
# https://api.aitutor.live/v1/login


@app.get("/")  # this is a test endpoint just to see if it working
async def read_root():
    return {"Hello": "World"}


@app.get("/key")
async def get_key(api_key_value: dict = Depends(check_api_key)):
    return api_key_value


@app.get("/test_user")
async def test_user():
    users = await app.mongodb["users"].find().to_list(None)
    # Convert ObjectId to string
    for user in users:
        # TODO: implement modeling to avoid this
        # This is just a workaround for now
        user["_id"] = str(user["_id"])
    return users


@app.post("/token")  # copied from chatgpt
async def create_token(token_data: Token, api_key_value: dict = Depends(check_api_key)):
    """
    Returns base64 encoded JSON Web Token
    """
    access_token = create_access_token(data={"sub": token_data.sub, "uni": token_data.uni})
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/user")  # copied from chatgpt
# async def get_user(token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)):
#     return await get_user_from_token(token)


@app.get("/user", response_model=User)
async def get_user(token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)):
    return await get_user_from_token(token)


@app.post("/v1/ingest")
async def ingest_data(user_data: CanvasData):
    user_dict = user_data.dict(exclude_none=True)
    users = await app.mongodb["users"].update_one(
        {"canvas_id": user_dict["canvas_id"], "institution": user_dict["institution"]}, {"$set": user_dict}, upsert=True
    )
    print(users)


@app.post("/v1/chat")
async def chat(messages: List[Message], api_key_value: dict = Depends(check_api_key)):
    completion = await app.openai.chat.completions.create(
        messages=SYSTEM_MESSAGE + messages,
        model=CHAT_MODEL,
        temperature=0.7,
        top_p=0.9,
    )
    return completion.choices[0].message


@app.post("/v1/chat_stream")
async def chat_stream(messages: List[Message], api_key_value: dict = Depends(check_api_key)):
    async def iter_response(messages):
        completion = await app.openai.chat.completions.create(
            messages=SYSTEM_MESSAGE + messages,
            model=CHAT_MODEL,
            logprobs=True,
            stream=True,
            temperature=0.7,
            top_p=0.9,
            # stream_options={"include_usage": True}, # currently errors out
        )
        async for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                yield json.dumps({"content": chunk.choices[0].delta.content})

    return StreamingResponse(iter_response(messages), media_type="application/json")


@app.post("/v1/smart_chat_stream")
async def smart_chat_stream(
    messages: List[Message], token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)
):
    user = await get_user_from_token(token)

    fields = ["kind", "title", "html_url"]
    context = [{f: a[f]} for f in fields for a in user["activity_stream"]]
    formatted_context = [
        {
            "role": "user",
            "content": f"Recent canvas updates at {user["institution"]}: {json.dumps(context)}",
        }
    ]

    async def iter_response(messages):
        response = await app.openai.chat.completions.create(
            messages=SYSTEM_MESSAGE + formatted_context + messages,
            model=CHAT_MODEL,
            logprobs=True,
            stream=True,
            temperature=0.7,
            top_p=0.9,
            # stream_options={"include_usage": True}, # currently errors out
        )

        completion = ""
        tool_calls = []
        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                completion += delta.content
                yield json.dumps({"content": chunk.choices[0].delta.content})

            elif delta and delta.tool_calls:
                for tool in delta.tool_calls:
                    if len(tool_calls) <= tool.index:
                        tool_calls.append(
                            {
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                            }
                        )

                        tc = tool_calls[tool.index]

                        if tool.id:
                            tc["id"] += tool.id

                        if tool.function.name:
                            tc["function"]["name"] += tool.function.name

                        if tool.function.arguments:
                            tc["function"]["arguments"] += tool.function.arguments

        if tool_calls:
            messages.append({"role": "assistant", "content": completion, "tool_calls": tool_calls})

            for tc in tool_calls:
                function_name = tc["function"]["name"]

                if tc["function"]["arguments"]:
                    function_args = json.loads(tc["function"]["arguments"])
                else:
                    function_args = {}

                # TODO: Call functions

    return StreamingResponse(iter_response(messages), media_type="application/json")


# NOTE: we need to define the data that the endpoint takes, just like a function call
# we need to figure out the required and not required parameters for each

# TODO: | /v1/login
#       | /v1/logout
# just an endpoint(s) to login/logout

# TODO: | /v1/message
# get a message from the tutor aka send a message to the tutor and get a response back
