"""AI unit tests with local stubs (no real external deps).

Stubs are pre-loaded in conftest.py before any imports, so they are available here.
"""
import json
import asyncio

import pytest

from ai import (
	openai_iter_response,
	openai_formatted_iter_response,
	get_assignments,
	get_activity_stream,
	get_overall_grades,
)
from models import Message  # noqa: E402
from types import SimpleNamespace


@pytest.mark.asyncio
async def test_openai_iter_response_streams(fake_openai, mock_moderate):
	"""Streams unflagged tokens from the OpenAI stub."""

	mock_moderate.return_value = SimpleNamespace(flagged=False)
	context = {"user": {"bio": ""}, "courses": [], "activity_stream": []}
	messages = [Message(role="user", content="Hello!")]

	chunks = [c async for c in openai_iter_response(messages, "", context)]

	assert "".join(chunks) == "stub-response"


@pytest.mark.asyncio
async def test_openai_iter_response_flagged_self_harm(fake_openai, mock_moderate):
	"""Moderation flagged for self-harm should short-circuit with a resource message."""

	mock_moderate.return_value = SimpleNamespace(
		flagged=True,
		categories=SimpleNamespace(dict=lambda: {"self-harm": True}),
	)
	context = {
		"user": {"bio": "", "first_name": "T", "last_name": "User", "canvas_id": 1},
		"courses": [],
		"activity_stream": [],
	}
	messages = [Message(role="user", content="I feel bad")]

	chunks = [c async for c in openai_iter_response(messages, "", context)]

	assert chunks == [
		"I am worried you might not be doing too well, we have some [awesome resources](https://www.uvu.edu/studenthealth/) 🤍"
	]


@pytest.mark.asyncio
async def test_openai_formatted_iter_response_wraps(monkeypatch):
	"""Formatted wrapper should JSON-wrap content yielded by openai_iter_response."""

	async def fake_iter(messages, descriptions, context, model="gpt-4.1", recursive=False):
		for t in ["A", "B", "C"]:
			yield t

	monkeypatch.setattr("ai.openai_iter_response", fake_iter)

	context = {"user": {"bio": ""}, "courses": [], "activity_stream": []}
	messages = [Message(role="user", content="hello")]

	chunks = [json.loads(c)["content"] async for c in openai_formatted_iter_response(messages, "", context)]

	assert "".join(chunks) == "ABC"


@pytest.mark.asyncio
async def test_openai_iter_response_flagged_sexual(fake_openai, mock_moderate):
	"""Moderation flagged for sexual content should short-circuit with warning message."""

	mock_moderate.return_value = SimpleNamespace(
		flagged=True,
		categories=SimpleNamespace(dict=lambda: {"sexual": True}),
	)
	context = {
		"user": {"bio": "", "first_name": "T", "last_name": "User", "canvas_id": 2},
		"courses": [],
		"activity_stream": [],
	}
	messages = [Message(role="user", content="inappropriate")]

	chunks = [c async for c in openai_iter_response(messages, "", context)]

	assert chunks == ["That is not cool bro"]


@pytest.mark.asyncio
async def test_openai_iter_response_flagged_graphic(fake_openai, mock_moderate):
	"""Moderation flagged for graphic content should short-circuit with resource link."""

	mock_moderate.return_value = SimpleNamespace(
		flagged=True,
		categories=SimpleNamespace(dict=lambda: {"graphic": True}),
	)
	context = {
		"user": {"bio": "", "first_name": "T", "last_name": "User", "canvas_id": 3},
		"courses": [],
		"activity_stream": [],
	}
	messages = [Message(role="user", content="violent")]

	chunks = [c async for c in openai_iter_response(messages, "", context)]

	assert chunks == ["[Click here](https://www.uvu.edu/studenthealth/)"]


def test_get_activity_stream_filters_and_sorts():
	context = {
		"activity_stream": [
			{"kind": "Message", "updated_at": "2024-01-02T10:00:00Z"},
			{"kind": "Submission", "updated_at": "2024-02-01T10:00:00Z"},
			{"kind": "Message", "updated_at": "2024-03-01T10:00:00Z"},
		]
	}
	res = asyncio.run(get_activity_stream(context, ["Message"]))
	data = json.loads(res)
	# Should filter to Message kinds and sort descending by updated_at
	assert [d["updated_at"] for d in data] == ["2024-03-01T10:00:00Z", "2024-01-02T10:00:00Z"]


def test_get_overall_grades_json_dump():
	context = {
		"user": {
			"courses": [
				{"name": "Math", "course_code": "MTH101", "current_score": 90},
				{"name": "CS", "course_code": "CS101", "current_score": 95},
			]
		}
	}
	res = asyncio.run(get_overall_grades(context))
	data = json.loads(res)
	assert data[0]["code"] == "MTH101"
	assert data[1]["grade"] == 95


def test_get_assignments_filters_completed_and_sorts():
	context = {
		"activity_stream": [{"assignment_id": 1, "score": 10}],
		"courses": [
			{
				"assignments": [
					{
						"id": 1,
						"name": "done",
						"description": "d",
						"due_at": "2024-01-02T00:00:00Z",
						"updated_at": "2024-01-02T00:00:00Z",
						"points_possible": 10,
						"html_url": "u1",
						"submission_types": [],
						"locked_for_user": False,
					},
					{
						"id": 2,
						"name": "pending",
						"description": "d2",
						"due_at": "2024-02-01T00:00:00Z",
						"updated_at": "2024-02-01T00:00:00Z",
						"points_possible": 10,
						"html_url": "u2",
						"submission_types": [],
						"locked_for_user": False,
					},
				]
			}
		],
	}
	res = asyncio.run(get_assignments(context))
	data = json.loads(res)
	# completed assignment id=1 should be filtered out
	assert len(data) == 1
	assert data[0]["name"] == "pending"
