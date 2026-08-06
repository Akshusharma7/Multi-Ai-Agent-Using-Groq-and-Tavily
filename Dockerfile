## Parent image
FROM python:3.10-slim

## Essential environment variables: Helps is realtime logging and prevents python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container 
WORKDIR /app

## Installing system dependancies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app
COPY . .

## Run setup.py and install the package in editable mode also remove the cache to reduce image size
RUN pip install --no-cache-dir -e .

# Used PORTS
EXPOSE 8501
EXPOSE 9999

# Run the app 
CMD ["python", "app/main.py"]