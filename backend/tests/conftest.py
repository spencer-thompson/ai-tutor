"""Shared pytest fixtures and stubs for backend tests.

Stubs are loaded here at conftest module load time to ensure they are available
before any test modules import main.py or ai.py.
"""
import os
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

# Set JWT_SECRET_KEY before any imports
if not os.getenv("JWT_SECRET_KEY"):
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-unit-tests"
# Set BACKEND_API_KEY_NAME to avoid pydantic validation errors
if not os.getenv("BACKEND_API_KEY_NAME"):
    os.environ["BACKEND_API_KEY_NAME"] = "X-Test-API-Key"

# --- Global stubs for all test modules ---

class _StubAsyncOpenAI:
    """Stub for openai.AsyncOpenAI supporting streaming and moderations."""

    def __init__(self, contents=None):
        self._contents = contents or []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
        self.moderations = SimpleNamespace(create=self._moderations)

    async def _create(self, *args, **kwargs):
        async def _gen():
            for c in self._contents:
                yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=c))])

        return _gen()

    async def _moderations(self, *args, **kwargs):
        return SimpleNamespace(results=[SimpleNamespace(categories=SimpleNamespace(dict=lambda: {}), flagged=False)])


class _StubAsyncAnthropic:
    """Stub for anthropic.AsyncAnthropic."""

    def __getattr__(self, name):
        async def _noop(*args, **kwargs):
            return None

        return _noop


class _StubMessage:
    """Stub for models.Message."""

    def __init__(self, role: str = "user", content: str = ""):
        self.role = role
        self.content = content


class _StubModel:
    """Generic stub for models."""

    pass


class _StubAsyncIOMotorClient:
    """Stub for motor.motor_asyncio.AsyncIOMotorClient."""

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        """Make the client subscriptable to return a database."""
        return _StubDatabase()

    def get_database(self, *args, **kwargs):
        return _StubDatabase()

    async def command(self, *args, **kwargs):
        return {"ok": 1}

    async def drop_database(self, *args, **kwargs):
        """Stub for dropping a database."""
        return None

    def close(self):
        return None


class _StubDatabase:
    """Stub for MongoDB database."""

    def __getitem__(self, key):
        """Make the database subscriptable to return a collection."""
        return _StubCollection()

    def __getattr__(self, name):
        """Return a stub collection for any attribute access."""
        return _StubCollection()


class _StubCollection:
    """Stub for MongoDB collection."""

    async def find_one(self, *args, **kwargs):
        return None

    async def update_one(self, *args, **kwargs):
        return SimpleNamespace(modified_count=1)

    async def insert_one(self, *args, **kwargs):
        return SimpleNamespace(inserted_id="stub_id")

    def find(self, *args, **kwargs):
        """Return an async iterable stub."""
        return _StubCursor()


class _StubCursor:
    """Stub for MongoDB cursor."""

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration


# Pre-populate sys.modules with stubs before any test imports
_motor_asyncio_ns = SimpleNamespace(AsyncIOMotorClient=_StubAsyncIOMotorClient)

_models_ns = SimpleNamespace(
    Message=_StubMessage,
    AnalyticsRequest=_StubModel,
    CanvasCourse=_StubModel,
    CanvasData=_StubModel,
    Chat=_StubModel,
    Settings=_StubModel,
    Token=_StubModel,
    User=_StubModel,
    Assignment=_StubModel,
    Course=_StubModel,
    Rubric=_StubModel,
    UserCourse=_StubModel,
)

sys.modules.setdefault("openai", SimpleNamespace(AsyncOpenAI=_StubAsyncOpenAI))
sys.modules.setdefault("anthropic", SimpleNamespace(AsyncAnthropic=_StubAsyncAnthropic))
sys.modules.setdefault("markdownify", SimpleNamespace(markdownify=lambda x, **_: x))
sys.modules.setdefault("motor", SimpleNamespace(motor_asyncio=_motor_asyncio_ns))
sys.modules.setdefault("motor.motor_asyncio", _motor_asyncio_ns)
# Don't stub models - use real models module so FastAPI can validate properly
# sys.modules.setdefault("models", _models_ns)

# FastAPI stubs
class _StubFastAPI:
    def __init__(self, *args, **kwargs):
        pass

    def add_middleware(self, *args, **kwargs):
        return None

    def middleware(self, *args, **kwargs):
        def wrapper(fn):
            return fn

        return wrapper

    def __getattr__(self, name):
        def decorator(*args, **kwargs):
            def wrapper(fn):
                return fn

            return wrapper

        return decorator


class _StubDepends:
    def __init__(self, *args, **kwargs):
        pass


class _StubSecurity(_StubDepends):
    pass


class _StubHTTPException(Exception):
    def __init__(self, status_code=500, detail=""):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class _StubStatus:
    HTTP_401_UNAUTHORIZED = 401


class _StubAPIKeyHeader:
    def __init__(self, *args, **kwargs):
        pass


class _StubOAuth2PasswordBearer:
    def __init__(self, *args, **kwargs):
        pass


class _StubStreamingResponse:
    def __init__(self, *args, **kwargs):
        pass


# Import real TestClient for legacy integration tests
try:
    from fastapi.testclient import TestClient as _RealTestClient
except ImportError:
    # Fallback if fastapi not installed
    _RealTestClient = None

_fastapi_testclient_ns = SimpleNamespace(TestClient=_RealTestClient) if _RealTestClient else SimpleNamespace()

_fastapi_ns = SimpleNamespace(
    Depends=_StubDepends,
    FastAPI=_StubFastAPI,
    HTTPException=_StubHTTPException,
    Security=_StubSecurity,
    status=SimpleNamespace(HTTP_401_UNAUTHORIZED=_StubStatus.HTTP_401_UNAUTHORIZED),
    testclient=_fastapi_testclient_ns,  # Add testclient module to stub
)
_fastapi_security_ns = SimpleNamespace(APIKeyHeader=_StubAPIKeyHeader, OAuth2PasswordBearer=_StubOAuth2PasswordBearer)
_fastapi_responses_ns = SimpleNamespace(StreamingResponse=_StubStreamingResponse)
class _StubCORSMiddleware:
    """Stub for FastAPI CORSMiddleware."""
    def __init__(self, app, **kwargs):
        self.app = app

    async def __call__(self, scope, receive, send):
        """ASGI3 application callable."""
        await self.app(scope, receive, send)

_fastapi_cors_ns = SimpleNamespace(CORSMiddleware=_StubCORSMiddleware)

sys.modules.setdefault("fastapi", _fastapi_ns)
sys.modules.setdefault("fastapi.testclient", _fastapi_testclient_ns)  # Also stub the submodule
sys.modules.setdefault("fastapi.security", _fastapi_security_ns)
sys.modules.setdefault("fastapi.responses", _fastapi_responses_ns)
sys.modules.setdefault("fastapi.middleware", SimpleNamespace(cors=_fastapi_cors_ns))
sys.modules.setdefault("fastapi.middleware.cors", _fastapi_cors_ns)


# --- Pytest fixtures ---

@pytest.fixture
def fake_openai(monkeypatch):
    """Provide a fake OpenAI client and monkeypatch `ai.openai`."""
    # Initialize with default stub response content
    client = _StubAsyncOpenAI(contents=["s", "t", "u", "b", "-", "r", "e", "s", "p", "o", "n", "s", "e"])
    monkeypatch.setattr("ai.openai", client, raising=False)
    return client


@pytest.fixture
def fake_anthropic(monkeypatch):
    """Provide a fake Anthropic client and monkeypatch `ai.anthropic`."""
    client = _StubAsyncAnthropic()
    monkeypatch.setattr("ai.anthropic", client, raising=False)
    return client


@pytest.fixture
def mock_moderate(monkeypatch):
    """Monkeypatch ai.moderate to a controllable AsyncMock."""
    mocked = AsyncMock()
    monkeypatch.setattr("ai.moderate", mocked, raising=False)
    return mocked
