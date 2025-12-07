"""JWT and token utility tests."""
import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from main import create_access_token


class TestTokenUtils:
	"""Test JWT token creation and validation."""

	def test_create_access_token_basic(self):
		"""Token creation with basic claims."""
		token = create_access_token({"sub": "user123"})
		assert isinstance(token, str)
		assert len(token) > 0

	def test_token_contains_exp_claim(self):
		"""Created token should contain exp (expiration) claim."""
		token = create_access_token({"sub": "test"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "exp" in decoded
		assert "iat" in decoded

	def test_token_exp_is_future(self):
		"""Token expiration should be in the future."""
		token = create_access_token({"sub": "test"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
		now = datetime.now(timezone.utc)
		assert exp_time > now

	def test_token_exp_approximately_24_hours(self):
		"""Token should expire in approximately 24 hours."""
		token = create_access_token({"sub": "test"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
		now = datetime.now(timezone.utc)
		delta = exp_time - now
		# Should be between 20-28 hours (accounting for rounding)
		assert timedelta(hours=20) < delta < timedelta(hours=28)

	def test_token_preserves_custom_claims(self):
		"""Token should preserve all custom claims passed in."""
		claims = {"sub": "user456", "uni": "uvu", "role": "student"}
		token = create_access_token(claims)
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["sub"] == "user456"
		assert decoded["uni"] == "uvu"
		assert decoded["role"] == "student"

	def test_token_multiple_claim_types(self):
		"""Token can contain mixed claim types."""
		claims = {
			"sub": "user",
			"canvas_id": 123,
			"is_admin": False,
			"courses": [1, 2, 3],
		}
		token = create_access_token(claims)
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["canvas_id"] == 123
		assert decoded["is_admin"] is False
		assert decoded["courses"] == [1, 2, 3]

	def test_token_decode_with_wrong_secret_fails(self):
		"""Token cannot be decoded with wrong secret."""
		token = create_access_token({"sub": "test"})
		with pytest.raises(jwt.InvalidSignatureError):
			jwt.decode(token, "wrong-secret", algorithms=["HS256"])

	def test_token_decode_with_wrong_algorithm_fails(self):
		"""Token cannot be decoded with wrong algorithm."""
		token = create_access_token({"sub": "test"})
		with pytest.raises(jwt.InvalidAlgorithmError):
			jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS512"])

	def test_token_iat_is_now(self):
		"""Token iat (issued at) should be approximately now."""
		now_before = datetime.now(timezone.utc)
		token = create_access_token({"sub": "test"})
		now_after = datetime.now(timezone.utc)

		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		iat_time = datetime.fromtimestamp(decoded["iat"], tz=timezone.utc)

		# iat should be between before and after (with 1 second tolerance)
		tolerance = timedelta(seconds=1)
		assert now_before - tolerance <= iat_time <= now_after + tolerance

	def test_token_empty_claims_dict(self):
		"""Token creation with empty claims dict."""
		token = create_access_token({})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		# Should still have exp and iat
		assert "exp" in decoded
		assert "iat" in decoded

	def test_token_large_claim_value(self):
		"""Token can handle large claim values."""
		large_value = "x" * 10000
		token = create_access_token({"sub": "test", "data": large_value})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["data"] == large_value

	def test_token_special_characters_in_claims(self):
		"""Token preserves special characters in claims."""
		special = "test@#$%^&*()🎉"
		token = create_access_token({"sub": special})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["sub"] == special

	def test_token_nested_dict_claim(self):
		"""Token can contain nested dict claims."""
		token = create_access_token({
			"sub": "user",
			"metadata": {"org": "uvu", "dept": "CS"}
		})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["metadata"]["org"] == "uvu"
		assert decoded["metadata"]["dept"] == "CS"

	def test_token_idempotency(self):
		"""Multiple calls with same input produce same claims (except timestamps)."""
		claims = {"sub": "user123", "role": "admin"}
		token1 = create_access_token(claims)
		token2 = create_access_token(claims)

		decoded1 = jwt.decode(token1, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		decoded2 = jwt.decode(token2, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

		# User claims should match
		assert decoded1["sub"] == decoded2["sub"]
		assert decoded1["role"] == decoded2["role"]
		# But timestamps will differ slightly
		assert decoded1["iat"] >= decoded2["iat"]  # or vice versa
