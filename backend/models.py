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


class User(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None  # Make middle name optional
    email_address: str
    phone_number: str
    # roles: List[Role]  # user can have several roles


class Message(BaseModel):
    name: str
    role: Literal["user", "assistant"]
    content: str


class CanvasData(BaseModel):
    institution: str
    canvas_id: int
    first_name: str
    last_name: str
    avatar_url: str
    # effective_local: str
