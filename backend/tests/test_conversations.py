import pytest
from fastapi.testclient import TestClient
from main import app, create_access_token
from models import User

from tests.fixtures import test_db  # Import the fixture

client = TestClient(app)


@pytest.mark.asyncio
async def test_save_chat_session(test_db):
    """
    IT-BE-02: Verifies the /save_chat endpoint.
    - Creates a user directly in the database.
    - Generates a JWT for that user.
    - Sends a chat history to the /save_chat endpoint.
    - Asserts a 200 OK response.
    - Verifies the chat history was saved correctly in the database.
    """
    # 1. Create a test user in the database
    test_user_data = {
        "role": "student",
        "institution": "uvu",
        "canvas_id": 11223,
        "first_name": "Chat",
        "last_name": "Tester",
        "avatar_url": "http://example.com/avatar.png",
        "courses": [],
    }
    user_model = User(**test_user_data)
    await test_db["users"].insert_one(user_model.model_dump(by_alias=True))

    # 2. Generate a valid JWT for the test user
    token_data = {"sub": str(test_user_data["canvas_id"]), "uni": "uvu"}
    access_token = create_access_token(data=token_data)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Define a sample chat history and send it to the endpoint
    chat_history = [
        {"role": "user", "content": "Hello, AI Tutor!"},
        {"role": "assistant", "content": "Hello! How can I help you today?"},
    ]
    response = client.post("/save_chat", headers=headers, json=chat_history)

    # 4. Assert the API response
    assert response.status_code == 200

    # 5. Verify the database was updated correctly
    updated_user = await test_db["users"].find_one(
        {"canvas_id": test_user_data["canvas_id"]}
    )
    assert updated_user is not None
    assert "chat_history" in updated_user
    saved_history = updated_user["chat_history"]
    assert len(saved_history) == 2
    assert saved_history[0]["role"] == "user"
    assert saved_history[0]["content"] == "Hello, AI Tutor!"
    assert saved_history[1]["role"] == "assistant"