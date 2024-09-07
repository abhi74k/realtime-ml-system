# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to app
COPY pyproject.toml poetry.lock /app/

# Install dependencies from pyproject.toml and poetry.lock
RUN poetry install

# Copy the rest of the application code to the container
COPY . /app

# Set the timezone to New York
ENV TZ="America/New_York"

# Set the environment variable for the broker address
ENV BROKER_ADDRESS=redpanda-0:9092

# Set the environment variable to not buffer stdout
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["poetry", "run", "python", "src/MdProducer.py"]