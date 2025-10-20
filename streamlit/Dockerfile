# FROM python:latest
# FROM python:3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY ./requirements.txt .

# RUN pip install -r requirements.txt --upgrade
RUN uv pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# RUN python util.py
RUN uv run util.py

EXPOSE 8501
