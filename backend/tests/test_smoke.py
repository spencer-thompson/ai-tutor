from fastapi.testclient import TestClient

# The main.py file is in the parent directory, so we adjust the path
# to ensure the 'app' can be imported correctly by the test runner.
from main import app

client = TestClient(app)

def test_smoke_test():
    response = client.get("/")
    assert response.status_code == 200