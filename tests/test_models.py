import sys
from pathlib import Path
import pytest
from typing import List

# Make repo root importable so `backend` package can be imported when running tests from pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import pydantic  # type: ignore
except Exception:
    import pytest

    pytest.skip("pydantic is not installed in this environment; skipping User model unit tests", allow_module_level=True)

from backend.models import User, UserCourse, Settings
from pydantic import ValidationError


def make_minimal_user_payload() -> dict:
    return {
        "role": "student",
        "institution": "uvu",
        "canvas_id": 12345,
        "first_name": "Test",
        "last_name": "User",
        "avatar_url": "https://example.com/avatar.png",
        "courses": [
            {
                "id": 1,
                "name": "Intro",
                "role": "student",
                "institution": "uvu",
            }
        ],
    }


def test_user_model_validates_with_minimal_payload():
    """UT-BE-01: User Model Validation: should instantiate with correct payload."""
    payload = make_minimal_user_payload()
    user = User(**payload)

    assert user.first_name == "Test"
    assert user.canvas_id == 12345
    assert isinstance(user.courses, List.__class__) or isinstance(user.courses, list)


def test_user_model_raises_on_missing_required_fields():
    """UT-BE-02: Invalid User Model: missing required fields should raise ValidationError."""
    payload = {"canvas_id": 12345}  # missing first_name, last_name, etc.

    with pytest.raises(ValidationError):
        User(**payload)
