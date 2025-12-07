"""Negative and edge case unit tests for AI, auth, and token logic."""
import os
import pytest
import jwt
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from main import create_access_token


# --- Token negative/edge cases ---
def test_create_access_token_missing_sub():
	# Should raise KeyError or produce token without sub
	token = create_access_token({})
	decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
	# sub is not required, but should not be present
	assert "sub" not in decoded


def test_create_access_token_invalid_claim_type():
	# Should handle non-serializable claim values
	class NotSerializable:
		pass
	with pytest.raises(TypeError):
		create_access_token({"sub": NotSerializable()})


def test_decode_token_with_invalid_signature():
	token = create_access_token({"sub": "user"})
	with pytest.raises(jwt.InvalidSignatureError):
		jwt.decode(token, "wrong-secret", algorithms=["HS256"])


def test_decode_token_with_expired_token():
	# Create a token that expired yesterday
	now = datetime.now(timezone.utc)
	expired = now - timedelta(days=1)
	claims = {"sub": "user", "exp": int(expired.timestamp()), "iat": int((expired - timedelta(hours=1)).timestamp())}
	token = jwt.encode(claims, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
	with pytest.raises(jwt.ExpiredSignatureError):
		jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])


def test_decode_token_with_malformed_token():
	with pytest.raises(jwt.DecodeError):
		jwt.decode("not.a.jwt", os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])


# --- AI moderation edge cases ---
from ai import openai_iter_response
from models import Message

import asyncio


@pytest.mark.asyncio
@pytest.mark.xfail(reason="openai_iter_response crashes on empty messages (BR-006)")
async def test_openai_iter_response_empty_messages(fake_openai, mock_moderate):
	# Should yield nothing if messages is empty
	context = {"user": {"bio": ""}, "courses": [], "activity_stream": []}
	messages = []
	chunks = [c async for c in openai_iter_response(messages, "", context)]
	assert chunks == []


@pytest.mark.asyncio
async def test_openai_iter_response_flagged_multiple_categories(fake_openai, mock_moderate):
	# Moderation flagged for multiple categories
	mock_moderate.return_value = SimpleNamespace(
		flagged=True,
		categories=SimpleNamespace(dict=lambda: {"self-harm": True, "sexual": True, "graphic": True}),
	)
	context = {"user": {"bio": "", "first_name": "T", "last_name": "User", "canvas_id": 1}, "courses": [], "activity_stream": []}
	messages = [Message(role="user", content="bad stuff")]  # Should trigger moderation
	chunks = [c async for c in openai_iter_response(messages, "", context)]
	# Should return the self-harm resource message (first match)
	assert any("uvu.edu/studenthealth" in c for c in chunks)



# --- AI helper edge/negative cases ---
import ai
from httpx import Response


@pytest.mark.asyncio
async def test_get_markdown_webpage_invalid_url(monkeypatch):
	# Patch AsyncClient.get to simulate a failed request
	async def fake_get(self, url):
		class FakeResp:
			text = ''
		return FakeResp()
	monkeypatch.setattr(ai.AsyncClient, "get", fake_get)
	result = await ai.get_markdown_webpage(["http://bad-url"])
	assert isinstance(result, list)
	assert result[0] == {"http://bad-url": ''} or isinstance(result[0], Exception)


@pytest.mark.asyncio
async def test_get_python_result_handles_error(monkeypatch):
	# Patch AsyncClient.post to simulate error response
	async def fake_post(self, url, json):
		class FakeResp:
			text = 'error'
		return FakeResp()
	monkeypatch.setattr(ai.AsyncClient, "post", fake_post)
	result = await ai.get_python_result("raise Exception()")
	assert result == 'error'


import pytest


@pytest.mark.asyncio
async def test_get_overall_grades_empty_user():
	# Should return '[]' if no user in context
	context = {}
	result = await ai.get_overall_grades(context)
	assert result == '[]'


@pytest.mark.asyncio
async def test_get_activity_stream_empty_context():
	# Should return '[]' if no activity_stream
	context = {}
	result = await ai.get_activity_stream(context, ["Message"])
	assert result == '[]'


@pytest.mark.asyncio
async def test_get_assignments_empty_courses():
	# Should return '[]' if no courses
	context = {"courses": [], "activity_stream": []}
	result = await ai.get_assignments(context)
	assert result == '[]'
