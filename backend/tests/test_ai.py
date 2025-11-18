import pytest
from unittest.mock import AsyncMock, MagicMock

from ai import openai_iter_response
from models import Message

@pytest.mark.asyncio
async def test_openai_iter_response_with_mock(mocker):
    """
    UT-BE-03: Tests the AI response function using a mock.
    - Mocks the OpenAI API client.
    - Asserts that the function correctly processes the mock response.
    - Asserts that the OpenAI client was called with the correct model and messages.
    """
    # 1. Mock the OpenAI client's create method
    mock_openai_create = mocker.patch(
        "ai.openai.chat.completions.create", new_callable=AsyncMock
    )

    # 2. Define a mock response object
    mock_chunk = MagicMock()
    mock_chunk.choices[0].delta.content = "This is a mocked AI response."

    async def mock_stream():
        yield mock_chunk

    mock_openai_create.return_value = mock_stream()

    # 3. Call the function with sample messages
    sample_messages = [Message(role="user", content="Hello, AI Tutor!")]
    # Provide minimal context required for the function to run
    context = {
        "user": {"settings": {"bio": ""}, "courses": []},
        "courses": [],
        "activity_stream": [],
    }
    descriptions = ""

    # Collect the streamed response
    response_chunks = [
        chunk async for chunk in openai_iter_response(sample_messages, descriptions, context)
    ]
    response = "".join(response_chunks)

    # 4. Assert that the function returns the mocked content
    assert response == "This is a mocked AI response."

    # 5. Assert that the OpenAI client was called correctly
    call_args, call_kwargs = mock_openai_create.call_args
    assert call_kwargs["model"] == "gpt-4.1"
    assert call_kwargs["messages"][-1].content == sample_messages[-1].content