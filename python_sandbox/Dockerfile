# FROM python:3.13
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# COPY ./requirements.txt .
#
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy dependencies
COPY ./pyproject.toml .
COPY ./uv.lock .

# Update dependencies
RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8081
