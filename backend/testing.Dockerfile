# Use the same base image as the fastapi service for consistency
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install uv, the python package manager/runner
RUN pip install uv

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install production and development dependencies
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system -r requirements-dev.txt

# Copy the backend application code
COPY . .

# Set the default command to run pytest
CMD ["pytest"]