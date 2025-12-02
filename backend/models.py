from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict, List, Literal, Optional

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

    role: Optional[Literal["Auto", "Tutor", "General", "Quick"]] = "Auto"
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
