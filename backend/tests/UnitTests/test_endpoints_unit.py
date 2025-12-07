"""Unit tests for endpoint handler logic using stubs and monkeypatching."""
import pytest
from types import SimpleNamespace

import main


@pytest.fixture(autouse=True)
def patch_app(monkeypatch):
	# Patch app.mongodb with a fake users collection
	fake_users = {}
	class FakeCollection:
		def __init__(self):
			self.data = fake_users
		async def find(self):
			class Cursor:
				async def to_list(self, _):
					return list(self.data.values())
			return Cursor()
		def update_one(self, query, update, upsert=False):
			key = (query["canvas_id"], query["institution"])
			doc = update.get("$set", {})
			if "$setOnInsert" in update and key not in self.data:
				doc = {**update["$setOnInsert"], **doc}
			self.data[key] = doc
			return SimpleNamespace(upserted_id=key)
		def delete_one(self, query):
			key = (query["canvas_id"], query["institution"])
			deleted = self.data.pop(key, None)
			return SimpleNamespace(deleted_count=1 if deleted else 0)
	fake_db = {"users": FakeCollection()}
	# Set mongodb attribute directly if it doesn't exist
	if not hasattr(main.app, "mongodb"):
		main.app.mongodb = fake_db
	else:
		monkeypatch.setattr(main.app, "mongodb", fake_db)
	# Patch patterns and md for post_user
	if not hasattr(main.app, "patterns"):
		main.app.patterns = SimpleNamespace(clean_markdown=SimpleNamespace(subn=lambda r, s: (s, 1)))
	else:
		monkeypatch.setattr(main.app, "patterns", SimpleNamespace(clean_markdown=SimpleNamespace(subn=lambda r, s: (s, 1))))
	monkeypatch.setattr(main, "md", lambda x: x)
	return fake_db


@pytest.fixture
def fake_token(monkeypatch):
	# Patch get_user_from_token and get_user_id_from_token
	async def fake_get_user_from_token(token):
		return {"canvas_id": 1, "institution": "uvu", "name": "Test User"}
	monkeypatch.setattr(main, "get_user_from_token", fake_get_user_from_token)
	async def fake_get_user_id_from_token(token):
		return 1, "uvu"
	monkeypatch.setattr(main, "get_user_id_from_token", fake_get_user_id_from_token)



import asyncio

@pytest.mark.asyncio
async def test_get_user_returns_user(fake_token):
	# Should return the user dict from the stub
	result = await main.get_user(token="fake", api_key_value={})
	assert result == {"canvas_id": 1, "institution": "uvu", "name": "Test User"}


@pytest.mark.asyncio
async def test_save_chat_session_updates_db(fake_token, patch_app):
	# Should update chat_history for the user
	messages = [SimpleNamespace(dict=lambda exclude_none=True: {"role": "user", "content": "hi"})]
	# Pre-populate user
	patch_app["users"].data[(1, "uvu")] = {"canvas_id": 1, "institution": "uvu"}
	# Call endpoint
	await main.save_chat_session(messages=messages, token="fake", api_key_value={})
	# Check chat_history updated
	user = patch_app["users"].data[(1, "uvu")]
	assert "chat_history" in user
	assert user["chat_history"] == [{"role": "user", "content": "hi"}]
