# FROM python:3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY ./requirements.txt .

RUN uv pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080
