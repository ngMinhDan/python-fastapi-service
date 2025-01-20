# Pull official base image
FROM python:3.10-slim

# Set work directory
WORKDIR /opt

# Set static environment variables
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .



# Environment variables for Uvicorn
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=80
ENV UVICORN_WORKERS=1

# Command: Pass environment variables dynamically
ENTRYPOINT ["sh", "-c", "uvicorn app:app --host $UVICORN_HOST --port $UVICORN_PORT --workers $UVICORN_WORKERS"]
