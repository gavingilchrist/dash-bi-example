# syntax = docker/dockerfile:1.2

# Get parent image
FROM python:3.9-slim
SHELL ["/bin/bash", "-c"]

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
WORKDIR /app
COPY app .

# Set and expose port
ENV SERVICE_PORT=8050
EXPOSE ${SERVICE_PORT}

# Copy secrets to .env file in container
RUN --mount=type=secret,id=dotenv \
  cp -r /run/secrets/dotenv /.env

# Run app server via Gunicorn
RUN python -m dashblox.setup
CMD gunicorn -b 0.0.0.0:${SERVICE_PORT} main:server
