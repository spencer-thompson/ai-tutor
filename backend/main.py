"""
FastAPI backend for the AI Tutor (webapp and mobile)

Reference: https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520

THOUGHTS:
- This is going to be the "brain" of the whole project, where everything connects together
  that being said we need to create a couple end points
"""

import json
import logging
import os
import re
from collections import namedtuple
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from itertools import zip_longest
from logging.config import dictConfig
from typing import List

import jwt
from ai import openai_iter_response
from anthropic import AsyncAnthropic
from config import LogConfig
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from markdownify import markdownify as md
from models import CanvasCourse, CanvasData, Chat, Message, Settings, Token, User
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


tools = []

dictConfig(LogConfig().dict())
logger = logging.getLogger("aitutor")


# --- INIT ---
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    """
    This just safely starts and stops FastAPI with mongo
    """

    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)  # setup mongo
    app.mongodb = app.mongodb_client.get_database("aitutor")
    ping_response = await app.mongodb.command("ping")

    app.openai = AsyncOpenAI()  # Setup OpenAI
    app.anthropic = AsyncAnthropic()

    app.patterns = namedtuple("Pattern", ["clean_markdown"])(re.compile(r"(\n){2,}"))

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    else:
        logger.info("Connected to database cluster.")

    yield

    app.mongodb_client.close()  # Shutdown


app = FastAPI(lifespan=db_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aitutor.live",
        "https://uvu.instructure.com",
        "http://localhost:8080",
        "http://localhost:5555",
        "chrome-extension://ndaaaojmnehkocealgfdaebakknpihcj",
        "chrome-extension://dkbedcgheicjblgfddhifhemjchjpkdl",
        "chrome-extension://dkbedcgheicjblgfddhifhemjchjpkdl",
        "chrome-extension://eoidpdhnopocccgnlclpmadnccolaman",
    ],  # List the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "frame-ancestors 'self' https://aitutor.live"
    return response


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
        id = int(id)  # fix updated pyjwt
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        user = await app.mongodb["users"].find_one({"canvas_id": id, "institution": uni})
        courses = (
            await app.mongodb["courses"]
            .find({"institution": uni, "id": {"$in": [c["id"] for c in user.get("courses")]}})
            .to_list(None)
        )

        catalog_courses = (
            await app.mongodb["catalog"]
            .find(
                {
                    "institution": uni,
                    "code": {"$in": [" ".join(c.get("name").split("-")[0:2]) for c in courses]},
                }
            )
            .to_list(None)
        )

        merged_courses = [
            {**c, **a} if " ".join(c.get("name").split("-")[0:2]) == a.get("code") else c
            for c, a in zip_longest(courses[:], catalog_courses, fillvalue={})
        ]

        user["courses"] = [u | c for u in user["courses"] for c in merged_courses if u["id"] == c["id"]]
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def get_user_id_from_token(token: str):
    """
    Returns a tuple of id, uni
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id = payload.get("sub")
        id = int(id)  # fix updated pyjwt
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        return id, uni

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


# --- V1 ENDPOINTS --- #


@app.get("/")  # this is a test endpoint just to see if it working
async def read_root():
    return {"Hello": "World"}


@app.get("/key")
async def get_key(api_key_value: dict = Depends(check_api_key)):
    return api_key_value


@app.get("/token")
async def refresh_token(token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)):
    """
    Returns a valid JSON Web Token.
    Uses the current token to generate, or refresh, a new one.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id = payload.get("sub")
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        new_token = create_access_token(data={"sub": id, "uni": uni})
        return {"token": new_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/token")
async def create_token(token_data: Token, api_key_value: dict = Depends(check_api_key)):
    """
    Returns a valid JSON Web Token.
    Currently, tokens expire after 1 day.
    """
    access_token = create_access_token(data={"sub": str(token_data.sub), "uni": token_data.uni})
    return {"token": access_token}


@app.get("/user", response_model=User)
async def get_user(token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)):
    """
    Returns the currently logged in user (from JWT)
    Strips away tons of course information.
    """
    return await get_user_from_token(token)


@app.post("/user")
async def post_user(user_data: CanvasData, api_key_value: dict = Depends(check_api_key)):
    user_dict = user_data.dict(exclude_none=True)

    for activity in user_dict["activity_stream"]:
        if message := activity.get("message"):
            activity["message"] = app.patterns.clean_markdown.subn(r"\n\n", md(message))[0]

    app.mongodb["users"].update_one(
        {"canvas_id": user_dict["canvas_id"], "institution": user_dict["institution"]},
        {"$set": user_dict, "$setOnInsert": {"role": "normal"}},
        upsert=True,
    )


@app.post("/user_settings")
async def update_user_settings(
    settings: Settings, token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)
):
    id, uni = await get_user_id_from_token(token)

    app.mongodb["users"].update_one(
        {"canvas_id": id, "institution": uni},
        {"$set": {"settings": settings.dict(exclude_none=True)}},
        upsert=True,
    )


@app.get("/user_count")
async def get_user_count(api_key_value: dict = Depends(check_api_key)):
    total_users = len(await app.mongodb["users"].find().to_list(None))
    return {"total_users": total_users}


@app.post("/course")
async def post_courses(course_data: CanvasCourse, api_key_value: dict = Depends(check_api_key)):
    course_dict = course_data.dict(exclude_none=True)

    if syllabus := course_dict.get("syllabus_body"):
        course_dict["syllabus_body"] = app.patterns.clean_markdown.subn(r"\n\n", md(syllabus))[0]

    if course_dict.get("assignments"):
        for assignment in course_dict.get("assignments"):
            if assignment.get("description"):
                assignment["description"] = app.patterns.clean_markdown.subn(
                    r"\n\n", md(assignment.get("description"))
                )[0]

    app.mongodb["courses"].update_one(
        {"id": course_dict["id"], "institution": course_dict["institution"]},
        {"$set": course_dict},
        upsert=True,
    )


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


@app.post("/v1/smart_chat")
async def smart_chat(chat: Chat, token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)):
    """
    Sends full response with smart features
    `{"content": "the ai response"}` or `{"flagged": bool}`
    """
    return {"content": "Not implemented yet"}


@app.post("/v1/smart_chat_stream")
async def smart_chat_stream(
    chat: Chat, token: str = Depends(oauth2_scheme), api_key_value: dict = Depends(check_api_key)
):
    """
    Sends back chunks as they are generated from the AI.
    Response is an iterator in the form of:
    `{"content": "the ai response"}` or `{"flagged": bool}`
    """
    user = await get_user_from_token(token)
    messages = chat.messages
    descriptions = "\n\n".join(  # This filters for only selected courses
        [
            " ".join(c.get("name").split("|")[0].split("-")[0:2])
            + f"(User is a {c.get("role")}):\n"
            + c.get("description")
            for c in user["courses"]
            if c["id"] in chat.courses
        ]
    )

    activity_context = [a for a in user["activity_stream"] if a["course_id"] in chat.courses]
    course_context = [c for c in user["courses"] if c["id"] in chat.courses]

    context = {"activity_stream": activity_context, "courses": course_context}
    # print(context)

    return StreamingResponse(openai_iter_response(messages, descriptions, context), media_type="application/json")
