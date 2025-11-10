import os
import time

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
def test_create_and_get_user_flow():
    """Integration test: start with a clean server (running locally), POST /user then GET /user with token.

    Requirements:
    - Backend server running and reachable at TEST_API_URL or http://localhost:8080
    - BACKEND_API_KEY and BACKEND_API_KEY_NAME env vars set (or tests will skip)
    - JWT_SECRET_KEY set so tokens can be created/decoded by the server
    """
    if not API_KEY or not API_KEY_NAME or not os.getenv("JWT_SECRET_KEY"):
        pytest.skip("Integration test requires BACKEND_API_KEY, BACKEND_API_KEY_NAME, and JWT_SECRET_KEY environment variables")

    if not _server_available(TEST_URL):
        pytest.skip(f"Backend not reachable at {TEST_URL}; start the server before running integration tests")

    # Construct a minimal CanvasData payload matching backend.models.CanvasData
    payload = {
        "institution": "uvu",
        "canvas_id": 99999999,
        "first_name": "Integration",
        "last_name": "Tester",
        "avatar_url": "https://example.com/avatar.png",
        "courses": [
            {"id": 1, "name": "Test Course", "course_code": "TEST 101", "role": "student", "institution": "uvu"}
        ],
        "activity_stream": [],
    }

    headers = {API_KEY_NAME: API_KEY}

    # Create/update user
    r = requests.post(TEST_URL + "/user", headers=headers, json=payload, timeout=5)
    assert r.status_code in (200, 201, 204), f"Unexpected status creating user: {r.status_code} {r.text}"

    # Create a token for that user via POST /token
    r = requests.post(TEST_URL + "/token", headers=headers, json={"sub": payload["canvas_id"], "uni": payload["institution"]}, timeout=5)
    assert r.status_code == 200, f"Failed to create token: {r.status_code} {r.text}"
    token = r.json().get("token")
    assert token

    # GET /user with the token
    auth_headers = {API_KEY_NAME: API_KEY, "Authorization": f"Bearer {token}"}
    r = requests.get(TEST_URL + "/user", headers=auth_headers, timeout=5)
    assert r.status_code == 200, f"Failed to get user: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("first_name") == payload["first_name"]
    assert body.get("last_name") == payload["last_name"]

    # Cleanup: delete the user
    r = requests.delete(TEST_URL + "/user", headers=auth_headers, timeout=5)
    # deletion may return 200 or 204
    assert r.status_code in (200, 204)
