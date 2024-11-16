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
from anthropic import AsyncAnthropic
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from markdownify import markdownify as md
from models import CanvasCourse, CanvasData, Chat, Message, Token, User
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

    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")

    else:
        info("Connected to database cluster.")

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
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await app.mongodb["users"].find_one({"canvas_id": id, "institution": uni})
        courses = await app.mongodb["courses"].find({"id": {"$in": [c["id"] for c in user["courses"]]}}).to_list(None)
        user["courses"] = [u | c for u in user["courses"] for c in courses if u["id"] == c["id"]]  # NOTE: not tested
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


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
            raise HTTPException(status_code=401, detail="Invalid token")

        new_token = create_access_token(data={"sub": id, "uni": uni})
        return {"token": new_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/token")
async def create_token(token_data: Token, api_key_value: dict = Depends(check_api_key)):
    """
    Returns a valid JSON Web Token.
    Currently, tokens expire after 1 day.
    """
    access_token = create_access_token(data={"sub": token_data.sub, "uni": token_data.uni})
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
            activity["message"] = md(message)

    app.mongodb["users"].update_one(
        {"canvas_id": user_dict["canvas_id"], "institution": user_dict["institution"]},
        {"$set": user_dict, "$setOnInsert": {"role": "normal"}},
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
        course_dict["syllabus_body"] = md(syllabus)

    if course_dict.get("assignments"):
        for assignment in course_dict["assignments"]:
            assignment["description"] = md(assignment["description"])

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

    fields = ["kind", "title", "message", "html_url", "score", "points_possible", "submission_comments"]
    activity_context = [
        {f: a.get(f)} for f in fields for a in user["activity_stream"] if a["course_id"] in chat.courses
    ]
    course_context = [
        {
            "name": " ".join(c.get("name").split("|")[0].split("-")[0:2]),
            "role": c.get("role"),
            "score": c.get("current_score"),
        }
        for c in user["courses"]
        if c["id"] in chat.courses
    ]

    context = (
        [
            {
                "role": "user",
                "content": f"""Canvas updates for {user.get("first_name")} at {user.get("institution")}: 
                {json.dumps(activity_context)}, 
                
                Course Info:
                {json.dumps(course_context)}""",
            }
        ]
        if chat.courses and len(messages) == 1
        else []
    )

    async def anthropic_iter_response(messages):
        messages = [{"role": m.role, "content": m.content} for m in messages]
        response = await app.anthropic.messages.create(
            max_tokens=8192,
            system=SYSTEM_MESSAGE[0].get("content"),
            messages=context + messages,
            model="claude-3-5-sonnet-20241022",
            stream=True,
            temperature=0.7,
            top_p=0.9,
        )

        async for event in response:
            if event.type == "content_block_delta":
                yield json.dumps({"content": event.delta.text})

    async def iter_response(messages):
        response = await app.openai.chat.completions.create(
            messages=SYSTEM_MESSAGE + context + messages,
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

    return StreamingResponse(anthropic_iter_response(messages), media_type="application/json")
