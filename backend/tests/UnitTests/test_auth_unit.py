"""Auth/unit tests with local stubs (no app code changes).

Stubs are pre-loaded in conftest.py before any imports.
"""
import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from main import create_access_token  # noqa: E402


def _decode(token: str):
	return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])


def test_create_access_token_contains_sub_and_exp():
	tok = create_access_token({"sub": "123", "uni": "uvu"})
	payload = _decode(tok)
	assert payload["sub"] == "123"
	assert payload["uni"] == "uvu"
	# exp should be within ~24h of now
	exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
	now = datetime.now(timezone.utc)
	delta = exp - now
	assert timedelta(hours=20) < delta < timedelta(hours=28)


def test_create_access_token_expiry_in_future():
	tok = create_access_token({"sub": "abc", "uni": "uvu"})
	payload = _decode(tok)
	exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
	now = datetime.now(timezone.utc)
	assert exp > now
