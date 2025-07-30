# pull official base image
FROM python:3.10-slim

# set work directory
WORKDIR /opt

# set static environment variables
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt .
RUN pip install -U pip setuptools wheel &&\
    pip install -r requirements.txt

# copy project
COPY app/ app/
COPY config/ config/

ENV OTEL_METRICS_EXPORTER=''
ENV OTEL_SERVICE_NAME='python-fastapi-service'

ENV UVICORN_LOG_CONFIG=config/log-config.yml

# command: use exec-format over shell-format
ENTRYPOINT ["uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

