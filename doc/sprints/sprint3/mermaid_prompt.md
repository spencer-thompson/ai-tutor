# main.py
```python
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
import sys
from collections import namedtuple
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from itertools import zip_longest
from typing import List

import jwt
from anthropic import AsyncAnthropic
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from httpx import AsyncClient
from markdownify import markdownify as md
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from openai import AsyncOpenAI
from pymongo.errors import ConnectionFailure, OperationFailure

from ai import openai_formatted_iter_response
from models import AnalyticsRequest, CanvasCourse, CanvasData, Chat, Message, Settings, Token, User
from responses import openai_formatted_responses_iter

BACKEND_API_KEY_NAME = os.getenv("BACKEND_API_KEY_NAME")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# --- Database Connection Details ---
# These are read from environment variables set in docker-compose.
MONGO_APP_USERNAME = os.getenv("MONGO_APP_USERNAME")
MONGO_APP_PASSWORD = os.getenv("MONGO_APP_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "aitutor")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE", "admin")
CHAT_MODEL = os.getenv("CHAT_MODEL")
DOMAIN = os.getenv("DOMAIN")
PLAUSIBLE_API_KEY = os.getenv("PLAUSIBLE_API_KEY")
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

logger = logging.getLogger("uvicorn")


# --- INIT ---
@asynccontextmanager
async def db_lifespan(app: FastAPI):
    """
    Safely starts and stops the FastAPI application, including the database connection.
    """

    app.log = logging.getLogger("uvicorn")
    app.log.info(f"--- API Started at [{DOMAIN}] ---")

    # --- Database Connection ---
    try:
        # Check for all required environment variables at startup
        required_vars = {
            "MONGO_APP_USERNAME": MONGO_APP_USERNAME,
            "MONGO_APP_PASSWORD": MONGO_APP_PASSWORD,
            "MONGO_HOST": MONGO_HOST,
            "MONGO_DATABASE": MONGO_DATABASE,
            "JWT_SECRET_KEY": JWT_SECRET_KEY,
            "BACKEND_API_KEY_NAME": BACKEND_API_KEY_NAME,
        }
        missing_vars = [key for key, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        mongo_uri = f"mongodb://{MONGO_APP_USERNAME}:{MONGO_APP_PASSWORD}@{MONGO_HOST}/?authSource={MONGO_AUTH_SOURCE}"
        redacted_uri = f"mongodb://{MONGO_APP_USERNAME}:<REDACTED>@{MONGO_HOST}/?authSource={MONGO_AUTH_SOURCE}"

        app.log.info("Attempting to connect to MongoDB...")
        app.log.info(f"Connection String: {redacted_uri}")

        app.mongodb_client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        await app.mongodb_client.admin.command("ping")  # Verifies connection and auth
        app.mongodb: AsyncIOMotorDatabase = app.mongodb_client[MONGO_DATABASE]

        app.log.info(f"Successfully connected to MongoDB database '{MONGO_DATABASE}'.")

    except (ValueError, ConnectionFailure, OperationFailure) as e:
        app.log.error(f"DATABASE CONNECTION FAILED: {e}")
        # Raising an exception during lifespan startup will prevent FastAPI from starting.
        raise RuntimeError("Could not connect to the database. Exiting.") from e

    app.openai = AsyncOpenAI()  # Setup OpenAI
    app.anthropic = AsyncAnthropic()

    app.patterns = namedtuple("Pattern", ["clean_markdown"])(re.compile(r"(\n){2,}"))

    yield

    app.mongodb_client.close()  # Shutdown
    app.log.info("--- API Stopped ---")


app = FastAPI(lifespan=db_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aitutor.live",
        "https://beta.aitutor.live",
        "https://uvu.instructure.com",
        "http://uvu.instructure.com",
        "http://localhost:8080",
        "http://localhost:5555",
        "http://localhost:5173",
        f"http://{DOMAIN}",
        f"https://{DOMAIN}",
        f"http://beta.{DOMAIN}",
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
    """
    Check to see if an API key is valid.
    """
    document = await app.mongodb["keys"].find_one({api_key: {"$exists": True}})
    if document:
        return [v for k, v in document.items() if k not in {"_id"}][0]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )


def create_access_token(data: dict):
    """
    Encode a new JWT using the canvas_id and university

    The tokens expire after 1 day
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=1)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_user_from_token(token: str):
    """
    Given a JWT token, checks if the token is valid.

    If it is valid, it returns the user document from the database.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id = payload.get("sub")
        id = int(id)  # fix updated pyjwt
        uni = payload.get("uni")
        if id is None or uni is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        user = await app.mongodb["users"].find_one({"canvas_id": id, "institution": uni})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_courses_list = user.get("courses")
        if not user_courses_list:
            # If user has no courses, no need to perform course merge logic.
            return user

        courses = (
            await app.mongodb["courses"]
            .find({"institution": uni, "id": {"$in": [c["id"] for c in user_courses_list]}})
            .to_list(None)
        )

        catalog_courses = (
            await app.mongodb["catalog"]
            .find(
                {
                    "institution": uni,
                    # "code": {"$in": [" ".join(c.get("name").split("-")[0:2]) for c in courses]},
                    "code": {
                        "$in": [
                            " ".join(c.get("course_code").split(" ")[0:2])
                            if c.get("course_code")
                            else " ".join(c.get("name").split("-")[0:2])
                            for c in courses
                        ]
                    },
                }
            )
            .to_list(None)
        )

        # Create a lookup map from the catalog data for efficient merging.
        catalog_map = {item["code"]: item for item in catalog_courses}

        # Create a map of the user's courses by ID for efficient updates.
        user_courses_map = {c["id"]: c for c in user_courses_list}

        # Iterate through the detailed courses and merge catalog data.
        for course in courses:
            course_code_str = (
                " ".join(course.get("course_code").split(" ")[0:2])
                if course.get("course_code")
                else " ".join(course.get("name").split("-")[0:2])
            )
            if course["id"] in user_courses_map and (catalog_entry := catalog_map.get(course_code_str)):
                # Merge the detailed course data and catalog data into the user's course entry.
                user_courses_map[course["id"]].update(course)
                user_courses_map[course["id"]].update(catalog_entry)

        user["courses"] = list(user_courses_map.values())
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


async def get_user_id_from_token(token: str):
    """
    Takes in a JWT token.

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
    """
    Test endpoint
    """
    return {"Hello": "World"}


@app.get("/health", tags=["System"])
async def health_check(request: Request):
    """
    Health check endpoint. Confirms API is running and can connect to the database.
    """
    try:
        # The 'ping' command is cheap and confirms connectivity and authentication.
        await request.app.mongodb.command("ping")
        return {"status": "ok", "database": "ok"}
    except Exception as e:
        # If this fails, it indicates a problem with the database connection.
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection error: {e}")


@app.get("/key")
async def get_key(api_key_value: dict = Depends(check_api_key)):
    """
    Get the value (notes) associated with an API key, if the key is valid.
    """
    return api_key_value


@app.get("/token")
async def refresh_token(token: str = Depends(oauth2_scheme)):
    """
    Returns a valid JSON Web Token.
    Uses the current token to generate or refresh, a new token.
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
async def get_user(token: str = Depends(oauth2_scheme)):
    """
    Returns the currently logged in user (from JWT)
    Strips away tons of course information.
    """
    return await get_user_from_token(token)


@app.post("/user")
async def post_user(user_data: CanvasData, api_key_value: dict = Depends(check_api_key)):
    """
    Add a new user into the database.
    """
    user_dict = user_data.dict(exclude_none=True)

    for activity in user_dict["activity_stream"]:
        if message := activity.get("message"):
            activity["message"] = app.patterns.clean_markdown.subn(r"\n\n", md(message))[0]

    app.mongodb["users"].update_one(
        {"canvas_id": user_dict["canvas_id"], "institution": user_dict["institution"]},
        {
            "$set": user_dict,
            "$setOnInsert": {
                "role": "normal",
                "settings": {
                    "bio": "",
                    "first_message": True,
                    "show_courses": True,
                    "notify_updates": True,
                    "shown_courses": {str(c["id"]): True for c in user_dict.get("courses")},
                },
            },
        },
        upsert=True,
    )


@app.delete("/user")
async def delete_user(token: str = Depends(oauth2_scheme)):
    """
    Delete All User Data for logged in User.
    """
    id, uni = await get_user_id_from_token(token)
    result = app.mongodb["users"].delete_one({"canvas_id": id, "institution": uni})
    return {"deleted_count": result.deleted_count}


@app.post("/user_settings")
async def update_user_settings(settings: Settings, token: str = Depends(oauth2_scheme)):
    id, uni = await get_user_id_from_token(token)

    app.mongodb["users"].update_one(
        {"canvas_id": id, "institution": uni},
        {"$set": {"settings": settings.dict(exclude_none=True)}},
        upsert=True,
    )


@app.post("/save_chat")
async def save_chat_session(messages: List[Message], token: str = Depends(oauth2_scheme)):
    """
    Saves the last chat message in the database.
    """
    id, uni = await get_user_id_from_token(token)

    app.mongodb["users"].update_one(
        {"canvas_id": id, "institution": uni},
        {"$set": {"chat_history": [message.dict(exclude_none=True) for message in messages]}},
        upsert=True,
    )


@app.get("/user_count")
async def get_user_count(api_key_value: dict = Depends(check_api_key)):
    """
    Returns the total amount of users.
    """
    total_users = len(await app.mongodb["users"].find().to_list(None))
    return {"total_users": total_users}


@app.post("/course")
async def post_courses(course_data: CanvasCourse, api_key_value: dict = Depends(check_api_key)):
    """
    Insert or update a course into the database.
    """
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


@app.get("/analytics_data")
async def get_all_analytics_data(api_key_value: dict = Depends(check_api_key)):
    users = await app.mongodb["users"].find().to_list(None)
    cleaned_users = [
        {k: v for k, v in u.items() if k != "_id" if k != "activity_stream" if k != "planner"} for u in users
    ]

    # return [v for k, v in document.items() if k not in {"_id"}][0]
    return cleaned_users


@app.get("/analytics")
async def get_analytics_data(data: AnalyticsRequest, api_key_value: dict = Depends(check_api_key)):
    """
    Get analytic data from Plausible.
    """
    url = "https://analytics.aitutor.live/api/v2/query"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {PLAUSIBLE_API_KEY}"}
    filters = [["is_not", "event:props:canvas_id", ["(none)"]]]
    # filters = [["is_not", "event:props:canvas_id", ["(none)"]], ["is_not", "event:props:length", ["(none)"]]]
    dimensions = [
        "event:props:canvas_id",
        "event:goal",
        # "event:props:length",
        # "event:props:id",
        # "event:page",
    ]
    if data.timeseries:
        dimensions.insert(1, "time:day")

    request_data = {
        "site_id": "aitutor.live",
        "metrics": ["events"],
        "filters": filters,
        "dimensions": dimensions,
        "date_range": [data.start, data.end],
    }

    async with AsyncClient() as client:
        r = await client.post(url, json=request_data, headers=headers)

    results = r.json().get("results")

    if not results:
        return r.json()

    if "event:props:canvas_id" in dimensions:
        canvas_ids = [int(i.get("dimensions")[0]) for i in results]

        matching_users = await app.mongodb["users"].find({"canvas_id": {"$in": canvas_ids}}).to_list(None)

        users = [
            {k: v for k, v in u.items() if k != "activity_stream" if k != "planner" if k != "chat_history"}
            for u in matching_users
        ]

        # TODO: The 'users' variable is populated but not yet used in the final response.
        # Future work could involve merging this user data with the analytics results.

    return r.json()


@app.post("/v1/chat")
async def chat(messages: List[Message], api_key_value: dict = Depends(check_api_key)):
    """
    Non streaming chat endpoint without extra features.
    """
    completion = await app.openai.chat.completions.create(
        messages=SYSTEM_MESSAGE + messages,
        model=CHAT_MODEL,
        temperature=0.7,
        top_p=0.9,
    )
    return completion.choices[0].message


@app.post("/v1/chat_stream")
async def chat_stream(messages: List[Message], api_key_value: dict = Depends(check_api_key)):
    """
    Streaming chat endpoint without any extra features.
    """

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
async def smart_chat(chat: Chat, token: str = Depends(oauth2_scheme)):
    """
    Sends full response with smart features
    `{"content": "the ai response"}` or `{"flagged": bool}`
    """
    return {"content": "Not implemented yet"}


@app.post("/v1/smart_chat_stream")
async def smart_chat_stream(chat: Chat, token: str = Depends(oauth2_scheme)):
    """
    Sends back chunks as they are generated from the AI.
    Response is an iterator in the form of:
    `{"content": "the ai response"}`
    """
    user = await get_user_from_token(token)
    messages = chat.messages
    model = chat.model
    course_descriptions = []
    # this processes data from the user and the database
    # and prepares it for the AI chat / function calling
    for c in user["courses"]:
        if c["id"] in chat.courses:
            if c.get("course_code"):
                name = " ".join(c.get("course_code").split(" ")[0:2])
            else:
                name = " ".join(c.get("name").split("|")[0].split("-")[0:2]) if c.get("name") else ""

            role = f"(User is a {c.get('role')})" if c.get("role") else ""
            desc = c.get("description") if c.get("description") else ""

            course_descriptions.append(f"### {name} - [{role}]:\n* {desc}")

    descriptions = "\n\n".join(course_descriptions)

    activity_context = [a for a in user["activity_stream"] if a["course_id"] in chat.courses]
    course_context = [c for c in user["courses"] if c["id"] in chat.courses]
    user_context = {
        "bio": user["settings"].get("bio"),
        "courses": user["courses"],
        "canvas_id": user.get("canvas_id"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
    }

    context = {"activity_stream": activity_context, "courses": course_context, "user": user_context}

    # return StreamingResponse(
    #     openai_formatted_iter_response(messages, descriptions, context, model), media_type="application/json"
    # )

    return StreamingResponse(
        openai_formatted_responses_iter(messages, descriptions, context), media_type="application/json"
    )
```


# models.py
```python
from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict, List, Literal, Optional

from pydantic import BaseModel, constr

# class UserModel(BaseModel):
#     """
#     Container for a single user
#     """

# The primary key for the StudentModel, stored as a `str` on the instance.
# This will be aliased to `_id` when sent to MongoDB,
# but provided as `id` in the API requests and responses.
# id: Optional[PyObjectId] = Field(alias="_id", default=None)


class Token(BaseModel):
    sub: str | int  # canvas_id
    uni: Literal["uvu"]  # can add more universities here


class Message(BaseModel):
    name: Optional[str] = None
    role: Literal["user", "assistant"]
    content: str


class Chat(BaseModel):
    """
    Format for any Smart Chat endpoints
    """

    messages: List[Message]
    courses: Optional[List[int]] = None
    model: Optional[Literal["gpt-4o", "gpt-4o-mini", "o1", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"]] = "gpt-4.1"


class Rubric(BaseModel):
    description: str
    points: float


class Assignment(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    due_at: Optional[str] = None
    updated_at: str
    points_possible: Optional[int] = None
    html_url: str
    rubric: Optional[List[Rubric]] = None
    lock_at: Optional[str] = None
    unlock_at: Optional[str] = None
    locked_for_user: bool
    submission_types: List[str]


class Course(BaseModel):
    id: int
    name: str
    course_code: Optional[str] = None
    role: str
    institution: str
    current_score: Optional[float] = None
    # syllabus_body: Optional[str] = None
    # assignments: Optional[List[Assignment]] = None
    # NOTE: can include more info


class CanvasCourse(BaseModel):
    id: int
    name: str
    course_code: Optional[str] = None
    institution: str
    syllabus_body: Optional[str] = None
    assignments: Optional[List[Assignment]] = None


class Settings(BaseModel):
    bio: Optional[str] = ""
    notify_updates: Optional[bool] = True
    first_message: Optional[bool] = True
    show_courses: Optional[bool] = True
    shown_courses: Optional[Dict[str, bool]] = None


class UserCourse(BaseModel):
    id: int
    name: str
    course_code: Optional[str] = None
    role: str
    institution: str
    current_score: Optional[float] = None
    # this is catalog stuff
    code: Optional[str] = None


# class History(BaseModel):
#     messages: List[Message]
# timestamp: Optional[str] = datetime.now(tz=timezone(timedelta(hours=-7))).isoformat()


class User(BaseModel):
    role: str
    institution: str
    canvas_id: int
    first_name: str
    last_name: str
    avatar_url: str
    courses: List[UserCourse]
    settings: Optional[Settings] = None
    chat_history: Optional[List[Message]] = None


class SubmissionComment(BaseModel):
    author_name: str
    comment: str


class Activity(BaseModel):
    id: int
    kind: str
    title: str
    message: Optional[str] = None
    html_url: str
    course_id: int
    created_at: str
    updated_at: str
    read_state: bool
    late: Optional[bool] = None
    missing: Optional[bool] = None
    seconds_late: Optional[int] = None
    score: Optional[float] = None
    assignment_id: Optional[int] = None
    points_possible: Optional[int] = None
    submission_comments: Optional[List[SubmissionComment]] = None


class PlannerItem(BaseModel):
    """
    Almost One to One map of the Canvas LMS Planner API.
    Some values are flattened for simplicity.
    https://canvas.instructure.com/doc/api/planner.html
    """

    canvas_id: Optional[int] = None
    context_type: str
    created_at: str
    updated_at: str
    excused: Optional[bool] = None
    graded: Optional[bool] = None
    has_feedback: Optional[bool] = None
    late: Optional[bool] = None
    missing: Optional[bool] = None
    needs_grading: Optional[bool] = None
    submitted: Optional[bool] = None
    plannable_date: str
    plannable_type: str
    title: str


class CanvasData(BaseModel):
    institution: str
    canvas_id: int
    first_name: str
    last_name: str
    avatar_url: str
    courses: List[Course]
    activity_stream: List[Activity]
    planner: Optional[List[PlannerItem]] = None
    # effective_local: str


class AnalyticsRequest(BaseModel):
    timeseries: Optional[bool] = False
    duration: Optional[bool] = False
    # metrics: Optional[List[Literal["events", "pageviews", "visitors"]]]
    # start: Annotated[str, constr(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    # end: Annotated[str, constr(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    start: str = datetime.now().strftime("%Y-%m-%d")
    end: str = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
```


# responses.py
```python
import asyncio
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from openai import AsyncOpenAI

from models import Message

MODEL = "gpt-5.1"
PATTERNS = [  # patterns for converting latex to markdown math
    {"rgx": re.compile(r"\\\s*?\(|\\\s*?\)", re.DOTALL), "new": r"$"},
    {"rgx": re.compile(r"\\\s*?\[|\\\s*?\]", re.DOTALL), "new": r"$$"},
]

openai = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# added_descriptions = (
#     f"## Courses\n\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
# )


def general_system_message(bio: str = "", descriptions: str = "") -> str:
    added_bio = f'## Customization\n\n"{bio}"\n- From the user' if bio else ""
    added_descriptions = (
        f"## Courses\n\nYou are an expert tutor in these courses: \n{descriptions}" if descriptions else ""
    )
    return f"""
    # Instructions

    You are the AI Tutor for **Utah Valley University** with a bright and excited attitude and tone.
    Respond in a concise and effictive manner.

    ## Formatting

    Formatting re-enabled — please use Markdown **bold**, _italics_, and header tags to **improve the readability** of your responses.

    {added_bio}

    {added_descriptions}

    ## Current Date and Time

    * {datetime.now(tz=timezone(timedelta(hours=-7))).strftime("%H:%M on %A, %Y-%m-%d")}
    """


def tutor_system_message():
    return """

    ## Tutoring

    When the student asks a question, do not respond with the answer.
    **Instead**, use the socratic method to tutor them and guide their thought process.

    Your responses should guide the student to learn the material in a fun, effective and friendly manner.
    Help the student think by asking one or two guiding questions.
    """


agent = {
    "name": "agent",
    "local": True,
    "func": None,
    "tool": {
        "type": "function",
        "name": "agent",
        "description": """
            Based on the user message, indicate which agent is needed to properly respond.
            If the user is asking a question related to coursework, or without providing context
            choose the Tutor agent, otherwise pick what seems best.
            If the user is asking to search the web use the assistant agent.
            Additionally, choose how much reasoning would be needed to effectively help the user,
            and how verbose, or long the output should be.
            """,
        "parameters": {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "description": "Which agent to choose from.",
                    "enum": ["Tutor", "Friend", "Assistant"],
                },
                "reasoning": {
                    "type": "string",
                    "description": "How much thinking time would provide the best response.",
                    "enum": ["none", "minimal", "low", "medium", "high"],
                },
                "verbosity": {
                    "type": "string",
                    "description": "How long of a response would be best. Most times lower is better.",
                    "enum": ["low", "medium", "high"],
                },
            },
            "required": [
                "agent",
                "reasoning",
                "verbosity",
            ],
        },
    },
}


async def moderate(message: str):
    """
    Moderate a string and return a warning if the message is bad.
    """
    response = await openai.moderations.create(
        input=message,
    )

    for result in response.results:
        if result.flagged:
            print("Flagged for moderation")

            categories = [cat for cat, flg in result.categories.dict().items() if flg]
            if any("self-harm" in c for c in categories):  # check for self-harm and send uvu student resources
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: self-harm"
                # )
                return "I am worried you might not be doing too well, we have some [awesome resources](https://www.uvu.edu/studenthealth/) 🤍"
            if any("sexual" in c for c in categories):  # check for sexual messages and stop them
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: sexual"
                # )
                return "That is not cool bro"
            if any("graphic" in c for c in categories):  # checks for graphic violence
                # logger.warning(
                #     f"STOPPED - {context['user'].get('first_name')} {context['user'].get('last_name')} ({context['user'].get('canvas_id')}) for: graphic"
                # )
                return "[Click here](https://www.uvu.edu/studenthealth/)"

    return ""


tools = []

tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in tools
}

agent_tools = [agent]

agent_tools = {
    tool.get("name"): {
        "tool": tool.get("tool"),
        "func": tool.get("func"),
        "local": tool.get("local"),
    }
    for tool in agent_tools
}


async def openai_formatted_responses_iter(messages: List[Dict[str, Dict]], descriptions, context):
    completion = ""
    previous_tokens = []
    sliding_window_limit = 3
    async for token in openai_responses_api_iter(messages=messages, descriptions=descriptions, context=context):
        previous_tokens.append(token)
        window_size = len(previous_tokens) if len(previous_tokens) <= sliding_window_limit else sliding_window_limit
        sliding_window = "".join(previous_tokens[-window_size:])

        for pat in PATTERNS:
            if match := pat["rgx"].search(sliding_window):
                previous_tokens = [sliding_window[: match.start()], pat["new"], sliding_window[match.end() :]]

        if len(previous_tokens) >= sliding_window_limit:
            popped_token = previous_tokens.pop(0)  # lol an actual stack in the wild
            completion += popped_token
            # yield popped_token
            yield json.dumps({"content": popped_token})

    if previous_tokens:  # flush out rest of sliding window
        for token in previous_tokens:
            completion += token
            # yield token
            yield json.dumps({"content": token})


async def openai_responses_api_iter(
    messages: List[Message],
    descriptions: str = "",
    context: dict = dict(),
    recursive=False,
):
    """
    New Responses API compatible with current code.
    Currently only uses GPT-5 and variants.
    """
    time_start = time.perf_counter()

    # filter out the "name" parameter
    messages = [{k: dict(m)[k] for k in ("role", "content")} for m in messages]
    first_message = messages[-1]

    mod = await moderate(first_message["content"])  # NOTE: this is a bit messy
    if mod:
        yield mod
        return

    time_after_moderation = time.perf_counter()

    # TODO: add time checks

    course_descriptions = f"## Courses\n\nThese are the student's courses: \n{descriptions}" if descriptions else ""

    if user := context.get("user"):
        bio = user.get("bio")
        if bio is None:
            bio = ""
    else:
        bio = ""

    agent_router = await openai.responses.create(
        model=MODEL,
        input=messages,
        tools=[t.get("tool") for t in agent_tools.values()],
        instructions=f"""
        Given an input message, determine which agent would most effectively help the user.
        Keep in mind you are providing these parameters for yourself in a future response.

        {course_descriptions}
        """,
        reasoning={"effort": "none"},
        tool_choice="required",
        store=False,  # retrieve later, defaults to true
    )

    # TODO: add time checks

    route = ""
    for output in agent_router.output:
        if output.type == "function_call":
            route = json.loads(output.arguments)
            # TODO: Get tokens used

    if route["agent"] == "Tutor":
        print(f"Using Agent: {route['agent']}")
        system_message = general_system_message(bio, descriptions) + tutor_system_message()
    else:
        system_message = general_system_message(bio, descriptions)

    print(f"Using Reasoning: {route['reasoning']}")
    print(f"Using Verbosity: {route['verbosity']}")
    print()

    stream = await openai.responses.create(
        model=MODEL,
        tools=[t.get("tool") for t in tools.values()],
        # tools=[t.get("tool") for t in tools.values()] + [{"type": "web_search"}],
        tool_choice="auto",
        input=messages,
        stream=True,
        instructions=system_message,
        reasoning={"effort": route["reasoning"]},
        text={"verbosity": route["verbosity"]},
        safety_identifier="Spencer",  # should be hashed string, incase they do something crazy
        store=False,  # retrieve later, defaults to true
    )

    async for event in stream:
        # print(event.type)
        if event.type == "response.created":
            time_response_created = time.perf_counter()

        if event.type == "response.output_text.delta":
            # print(event.delta, flush=True, end="")
            yield event.delta

        # # NOTE:
        # # This one is if we want the tokens for tool calls as they come in
        # # I don't really wanna mess with that though

        # if event.type == "response.function_call_arguments.delta":
        #     print(event)

        # if "response.output_item" in event.type:
        #     print(event)

        # TODO: Working on this now
        # if "response.web_search_call" in event.type:
        #     print(event)

        # if event.type == "response.web_search_call.completed":
        #     print(event)

        if event.type == "response.function_call_arguments.done":
            print("Calling tool")
            print(event.arguments)

        if event.type == "response.completed":
            time_response_completed = time.perf_counter()

            # print()
            # print(event)

            tokens_used = {
                "input_tokens": event.response.usage.input_tokens,
                "output_tokens": event.response.usage.output_tokens,
                "reasoning_tokens": event.response.usage.output_tokens_details.reasoning_tokens,
            }

    print()
    print()
    print(f"Start to end: {time_response_completed - time_start}")
    print(f"created to end: {time_response_completed - time_response_created}")

    # TODO: add recursive call?
    # Previously this was done on tool calls only


async def main() -> None:
    messages = [{"role": "user", "content": "Tell me a joke"}]
    async for event in openai_responses_api_iter(messages):
        print(event, flush=True, end="")


if __name__ == "__main__":
    asyncio.run(main())
```

This python code is in the FastAPI backend docker container, which is called from
a streamlit container which is the frontend.

Using the above code, create a mermaid diagram that shows all design patterns used in the code.


