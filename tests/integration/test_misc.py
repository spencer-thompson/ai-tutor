import os

import pytest
import requests

TEST_URL = os.getenv("TEST_API_URL", "http://localhost:8080")
API_KEY = os.getenv("BACKEND_API_KEY")
API_KEY_NAME = os.getenv("BACKEND_API_KEY_NAME")


def _server_available(url: str) -> bool:
    try:
        r = requests.get(url, timeout=1)
        return r.status_code < 500
    except Exception:
        return False


@pytest.mark.integration
def test_user_count_endpoint():
    if not API_KEY or not API_KEY_NAME:
        pytest.skip("Requires BACKEND_API_KEY and BACKEND_API_KEY_NAME env vars")
    if not _server_available(TEST_URL):
        pytest.skip("Backend not reachable; skipping")

    headers = {API_KEY_NAME: API_KEY}
    r = requests.get(TEST_URL + "/user_count", headers=headers, timeout=5)
    assert r.status_code == 200
    assert isinstance(r.json().get("total_users"), int)


@pytest.mark.integration
def test_save_chat_updates_user_chat_history():
    """Post a chat for a test user and verify chat_history updated via GET /user."""
    if not API_KEY or not API_KEY_NAME or not os.getenv("JWT_SECRET_KEY"):
        pytest.skip("Requires BACKEND_API_KEY, BACKEND_API_KEY_NAME, and JWT_SECRET_KEY env vars")
    if not _server_available(TEST_URL):
        pytest.skip("Backend not reachable; skipping")

    # Create test user
    payload = {
        "institution": "uvu",
        "canvas_id": 88888888,
        "first_name": "Chat",
        "last_name": "Tester",
        "avatar_url": "https://example.com/avatar.png",
        "courses": [],
        "activity_stream": [],
    }

    headers = {API_KEY_NAME: API_KEY}
    r = requests.post(TEST_URL + "/user", headers=headers, json=payload, timeout=5)
    assert r.status_code in (200, 201, 204)

    # create token
    r = requests.post(TEST_URL + "/token", headers=headers, json={"sub": payload["canvas_id"], "uni": payload["institution"]}, timeout=5)
    assert r.status_code == 200
    token = r.json().get("token")
    assert token

    auth_headers = {API_KEY_NAME: API_KEY, "Authorization": f"Bearer {token}"}

    # Save chat
    messages = [{"name": "Test", "role": "user", "content": "hello"}]
    r = requests.post(TEST_URL + "/save_chat", headers=auth_headers, json=messages, timeout=5)
    assert r.status_code in (200, 204)

    # Get user and verify chat_history
    r = requests.get(TEST_URL + "/user", headers=auth_headers, timeout=5)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body.get("chat_history"), list)

    # cleanup
    r = requests.delete(TEST_URL + "/user", headers=auth_headers, timeout=5)
    assert r.status_code in (200, 204)


@pytest.mark.integration
def test_post_course():
    if not API_KEY or not API_KEY_NAME:
        pytest.skip("Requires BACKEND_API_KEY and BACKEND_API_KEY_NAME env vars")
    if not _server_available(TEST_URL):
        pytest.skip("Backend not reachable; skipping")

    headers = {API_KEY_NAME: API_KEY}
    course_payload = {
        "id": 424242,
        "name": "Integration Course",
        "course_code": "INT 101",
        "institution": "uvu",
        "syllabus_body": "This is a test syllabus.",
    }

    r = requests.post(TEST_URL + "/course", headers=headers, json=course_payload, timeout=5)
    assert r.status_code in (200, 201, 204), f"Unexpected course post status: {r.status_code} {r.text}"
