from typing import List, Literal, Optional

from pydantic import BaseModel

# class UserModel(BaseModel):
#     """
#     Container for a single user
#     """

# The primary key for the StudentModel, stored as a `str` on the instance.
# This will be aliased to `_id` when sent to MongoDB,
# but provided as `id` in the API requests and responses.
# id: Optional[PyObjectId] = Field(alias="_id", default=None)


class Token(BaseModel):
    sub: int  # canvas_id
    uni: Literal["uvu"]  # can add more universities here


class Message(BaseModel):
    name: Optional[str] = None
    role: Literal["user", "assistant"]
    content: str


class Chat(BaseModel):
    messages: List[Message]
    courses: Optional[List[int]] = None


class Course(BaseModel):
    id: int
    name: str
    role: str
    current_score: float
    # TODO: Add institution


class CanvasCourse(BaseModel):
    id: int
    name: str
    institution: str
    syllabus_body: Optional[str] = None


class User(BaseModel):
    institution: str
    canvas_id: int
    first_name: str
    last_name: str
    avatar_url: str
    courses: List[Course]


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


class CanvasData(BaseModel):
    institution: str
    canvas_id: int
    first_name: str
    last_name: str
    avatar_url: str
    courses: List[Course]
    activity_stream: List[Activity]
    # effective_local: str
