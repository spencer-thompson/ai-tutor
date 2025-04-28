import os

import jwt
import requests

domain = os.getenv("DOMAIN")
api_key = os.getenv("BACKEND_API_KEY")
api_key_name = os.getenv("BACKEND_API_KEY_NAME")
jwt_secret = os.getenv("JWT_SECRET_KEY")

if "aitutor" in domain:
    url = f"https://api.{domain}"
else:
    url = f"http://api.{domain}"

r = requests.post(
    url + "/token",
    headers={api_key_name: api_key},
    json={"sub": 1948325, "uni": "uvu"},
    # json={}
)

valid_token = r.json()["token"]


def test_hello_world():
    r = requests.get(url)

    assert r.json() == {"Hello": "World"}


def test_no_api_key():
    r = requests.get(url + "/key")

    assert r.status_code != 200


def test_bad_api_key():
    r = requests.get(url + "/key", headers={api_key_name: "bad_key"})

    assert r.status_code != 200


def test_good_api_key():
    r = requests.get(url + "/key", headers={api_key_name: api_key})

    assert r.status_code == 200


def test_create_token():
    r = requests.post(
        url + "/token",
        headers={api_key_name: api_key},
        json={"sub": 1, "uni": "uvu"},
    )

    assert r.status_code == 200

    response = r.json()

    assert list(response.keys())[0] == "token"

    payload = jwt.decode(response["token"], jwt_secret, algorithms=["HS256"])

    assert payload.get("sub") == "1"
    assert payload.get("uni") == "uvu"


def test_bad_user():
    r = requests.get(
        url + "/user",
        headers={api_key_name: api_key, "Authorization": "Bearer 1"},
    )

    assert r.status_code != 200


def test_good_user():
    r = requests.get(
        url + "/user",
        headers={api_key_name: api_key, "Authorization": f"Bearer {valid_token}"},
    )

    assert r.status_code == 200
    assert r.json()["first_name"] == "Spencer"
    assert r.json()["last_name"] == "Thompson"


def test_user_count():
    r = requests.get(
        url + "/user_count",
        headers={api_key_name: api_key},
    )

    assert r.status_code == 200
    assert r.json().get("total_users") is not None
