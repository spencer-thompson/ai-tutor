"""Test-only stubs for external dependencies (OpenAI/Anthropic) and a simple in-memory DB.

These are used only from tests via monkeypatch and do not modify application code.
"""
from types import SimpleNamespace


class FakeChunk:
    """Represents a minimal streaming chunk with choices[0].delta.content."""

    def __init__(self, content: str):
        self.choices = [SimpleNamespace(delta=SimpleNamespace(content=content))]


class FakeAsyncOpenAI:
    """Minimal AsyncOpenAI stub with a chat.completions.create async generator."""

    def __init__(self, contents=None):
        # contents: list of strings to stream; default single token
        self._contents = contents or ["stub-response"]
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    async def _create(self, *args, **kwargs):
        async def _gen():
            for c in self._contents:
                yield FakeChunk(c)

        return _gen()

    async def close(self):
        return None


class FakeAsyncAnthropic:
    """Minimal Anthropic stub; methods return None or simple strings when awaited."""

    def __getattr__(self, name):
        async def _noop(*args, **kwargs):
            return None

        return _noop

    async def close(self):
        return None


class FakeCollection:
    """In-memory collection with minimal Mongo-like methods used in tests."""

    def __init__(self):
        self._docs = []

    async def insert_one(self, doc):
        self._docs.append(doc)
        return SimpleNamespace(inserted_id=len(self._docs))

    async def find_one(self, query):
        # naive match on equality of keys in query
        for d in self._docs:
            if all(d.get(k) == v for k, v in query.items()):
                return d
        return None

    async def update_one(self, query, update):
        matched = 0
        modified = 0
        for idx, d in enumerate(self._docs):
            if all(d.get(k) == v for k, v in query.items()):
                matched += 1
                if "$set" in update:
                    self._docs[idx] = {**d, **update["$set"]}
                    modified += 1
        return SimpleNamespace(matched_count=matched, modified_count=modified)


class FakeDB:
    """Minimal database stub with a 'users' collection attribute."""

    def __init__(self):
        self.users = FakeCollection()

    def __getitem__(self, item):
        if item == "users":
            return self.users
        raise KeyError(item)
