"""Comprehensive unit tests for utility and helper functions."""
import os
import pytest
from datetime import datetime, timedelta, timezone
import json

import jwt

from main import create_access_token


class TestEnvironmentConfiguration:
	"""Test environment variable handling and configuration."""

	def test_jwt_secret_key_is_set(self):
		"""JWT_SECRET_KEY must be set in environment."""
		assert os.getenv("JWT_SECRET_KEY") is not None
		assert len(os.getenv("JWT_SECRET_KEY")) > 0

	def test_jwt_secret_key_non_empty(self):
		"""JWT secret key should be non-empty string."""
		secret = os.getenv("JWT_SECRET_KEY")
		assert isinstance(secret, str)
		assert len(secret) > 5  # Reasonable minimum length

	def test_env_var_type_consistency(self):
		"""Environment variables should be strings."""
		jwt_secret = os.getenv("JWT_SECRET_KEY")
		assert isinstance(jwt_secret, str)


class TestTokenEdgeCases:
	"""Test edge cases and boundary conditions for token handling."""

	def test_token_with_null_characters_in_claims(self):
		"""Token should handle claims safely."""
		token = create_access_token({"sub": "user\x00test"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "sub" in decoded

	def test_token_with_numeric_sub(self):
		"""Token with numeric sub claim."""
		token = create_access_token({"sub": 999})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["sub"] == 999

	def test_token_with_zero_sub(self):
		"""Token with zero value."""
		token = create_access_token({"sub": 0})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["sub"] == 0

	def test_token_with_negative_number(self):
		"""Token can contain negative numbers."""
		token = create_access_token({"value": -42})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["value"] == -42

	def test_token_with_float_values(self):
		"""Token can contain floating point values."""
		token = create_access_token({"score": 95.5})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["score"] == 95.5

	def test_token_with_boolean_false(self):
		"""Token should preserve False boolean values."""
		token = create_access_token({"is_admin": False})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["is_admin"] is False

	def test_token_with_boolean_true(self):
		"""Token should preserve True boolean values."""
		token = create_access_token({"verified": True})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["verified"] is True

	def test_token_with_empty_string_claim(self):
		"""Token can contain empty string claims."""
		token = create_access_token({"bio": ""})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["bio"] == ""

	def test_token_with_unicode_emoji(self):
		"""Token preserves emoji and unicode."""
		token = create_access_token({"name": "User 🎉 😊"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "🎉" in decoded["name"]

	def test_token_with_json_like_string(self):
		"""Token can contain JSON-like string values."""
		json_str = '{"key": "value"}'
		token = create_access_token({"data": json_str})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["data"] == json_str

	def test_token_successive_creations_timestamps(self):
		"""Successive token creations may have same iat if created within same second."""
		token1 = create_access_token({"sub": "user", "v": 1})
		token2 = create_access_token({"sub": "user", "v": 2})

		decoded1 = jwt.decode(token1, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		decoded2 = jwt.decode(token2, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

		# iat timestamps might be the same if within same second
		# but tokens should differ due to different claims (v: 1 vs v: 2)
		assert decoded1["v"] == 1
		assert decoded2["v"] == 2

	def test_token_exp_before_iat_never_true(self):
		"""Expiration time should never be before issued-at time."""
		token = create_access_token({"sub": "user"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["exp"] > decoded["iat"]

	def test_token_with_very_long_list_claim(self):
		"""Token can contain long lists."""
		long_list = list(range(1000))
		token = create_access_token({"numbers": long_list})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert len(decoded["numbers"]) == 1000
		assert decoded["numbers"][999] == 999

	def test_token_multiple_claim_mutations(self):
		"""Creating tokens with incrementally modified claims."""
		claims = {"count": 0}
		tokens = []
		for i in range(5):
			claims["count"] = i
			token = create_access_token(claims.copy())
			tokens.append(token)

		# Each token should decode correctly
		for i, token in enumerate(tokens):
			decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
			assert decoded["count"] == i


class TestJWTStandardClaims:
	"""Test JWT standard claims (exp, iat, etc.)."""

	def test_token_has_exactly_exp_and_iat_from_create(self):
		"""Token from create_access_token should have exp and iat."""
		token = create_access_token({"sub": "user"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

		standard_claims = {"exp", "iat"}
		actual_keys = set(decoded.keys())

		assert standard_claims.issubset(actual_keys)

	def test_exp_is_unix_timestamp(self):
		"""exp should be a valid unix timestamp."""
		token = create_access_token({"sub": "user"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

		exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
		assert isinstance(exp_time, datetime)
		assert exp_time.year >= 2025

	def test_iat_is_unix_timestamp(self):
		"""iat should be a valid unix timestamp."""
		token = create_access_token({"sub": "user"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

		iat_time = datetime.fromtimestamp(decoded["iat"], tz=timezone.utc)
		assert isinstance(iat_time, datetime)
		assert iat_time.year >= 2025


class TestStringValueHandling:
	"""Test various string values in claims."""

	def test_token_with_quoted_string(self):
		"""Token with quoted values."""
		token = create_access_token({"name": '"quoted"'})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["name"] == '"quoted"'

	def test_token_with_single_quotes(self):
		"""Token with single quotes."""
		token = create_access_token({"name": "'single'"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["name"] == "'single'"

	def test_token_with_backslash(self):
		"""Token with backslash in string."""
		token = create_access_token({"path": "C:\\Users\\Test"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert decoded["path"] == "C:\\Users\\Test"

	def test_token_with_forward_slashes(self):
		"""Token with URL-like paths."""
		token = create_access_token({"url": "https://api.example.com/v1/users"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "https://" in decoded["url"]

	def test_token_with_newlines(self):
		"""Token can handle newlines in strings."""
		token = create_access_token({"text": "Line1\nLine2\nLine3"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "\n" in decoded["text"]

	def test_token_with_tabs(self):
		"""Token can handle tabs in strings."""
		token = create_access_token({"indented": "Row1\t\tValue1"})
		decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
		assert "\t" in decoded["indented"]
