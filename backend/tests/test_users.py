import pytest
from fastapi.testclient import TestClient
from main import app, create_access_token
from models import User
from datetime import timedelta

from tests.fixtures import test_db  # Import the fixture

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_current_user(test_db):
    """
    IT-BE-01: Verifies the /api/users/me endpoint.
    - Creates a user directly in the database.
    - Generates a JWT for that user.
    - Makes a request to the /api/users/me endpoint.
    - Asserts a 200 OK response and correct user data.
    """
    # 1. Create a test user in the database
    test_user_data = {
        "role": "student",
        "institution": "uvu",
        "canvas_id": 98765,
        "first_name": "Integration",
        "last_name": "Test",
        "avatar_url": "http://example.com/avatar.png",
        "courses": [],
    }
    user_model = User(**test_user_data)
    await test_db["users"].insert_one(user_model.model_dump(by_alias=True))

    # 2. Generate a valid JWT for the test user
    token_data = {"sub": str(test_user_data["canvas_id"]), "uni": "uvu"}
    access_token = create_access_token(data=token_data)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Make a GET request to /api/users/me
    response = client.get("/api/users/me", headers=headers)

    # 4. Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["canvas_id"] == test_user_data["canvas_id"]
    assert response_data["first_name"] == test_user_data["first_name"]
    assert response_data["role"] == test_user_data["role"]