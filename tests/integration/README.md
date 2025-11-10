Integration tests for backend + Mongo

How to run

1. Start Mongo (if not already):

   docker compose -f compose/mongo.yaml up -d

2. Start the backend server (local development):

   # from repo root
   cd backend
   # start with uvicorn or your preferred method; example using uvicorn:
   uvicorn main:app --reload --port 8080

3. Export required environment variables (example):

   export BACKEND_API_KEY_NAME=your_api_header_name
   export BACKEND_API_KEY=your_api_key_value
   export JWT_SECRET_KEY=your_jwt_secret
   # optionally override server URL
   export TEST_API_URL=http://localhost:8080

4. Run the integration test(s):

   pytest -q tests/integration/test_users.py

Notes
- The test will skip if the server is not reachable or the required env vars are missing.
- The test creates a transient user (canvas_id 99999999) and attempts to delete it at the end; if the server fails to delete, you may need to remove the document manually from the `aitutor.users` collection in your test Mongo.
