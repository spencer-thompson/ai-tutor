import pytest
from pydantic import ValidationError

from models import User, UserCourse, Settings


def test_user_model_creation():
    """
    Tests successful creation of a User model with valid data.
    """
    course_data = {
        "id": 101,
        "name": "Intro to Testing",
        "course_code": "CS 101",
        "role": "student",
        "institution": "uvu",
        "current_score": 95.5
    }
    user_data = {
        "role": "student",
        "institution": "uvu",
        "canvas_id": 12345,
        "first_name": "John",
        "last_name": "Doe",
        "avatar_url": "http://example.com/avatar.png",
        "courses": [course_data],
        "settings": {
            "bio": "A test user"
        }
    }

    user = User(**user_data)

    assert user.canvas_id == 12345
    assert user.first_name == "John"
    assert len(user.courses) == 1
    assert isinstance(user.courses[0], UserCourse)
    assert isinstance(user.settings, Settings)
    assert user.settings.bio == "A test user"


def test_user_model_invalid_data():
    """
    Tests that creating a User model with invalid data raises a ValidationError.
    """
    invalid_user_data = {
        "role": "student",
        "institution": "uvu",
        "canvas_id": "not-an-integer",  # Invalid data type
        "first_name": "Jane",
        "last_name": "Doe",
        "avatar_url": "http://example.com/avatar.png",
        "courses": []
    }

    with pytest.raises(ValidationError):
        User(**invalid_user_data)