Short test-run instructions

This repository includes a minimal smoke test that calls the backend endpoint directly (so it doesn't start FastAPI lifespan or connect to Mongo/OpenAI).

Quick local setup

1. Create and activate a virtual environment (recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install developer dependencies:

   pip install -r requirements-dev.txt

3. Run the smoke test:

   pytest -q

Notes
- The smoke test is `tests/test_smoke.py` and directly calls `backend.main.read_root()` to avoid external dependencies.
- For integration tests that require Mongo, start the local container before running tests (example: `docker compose -f compose/mongo.yaml up -d`).
