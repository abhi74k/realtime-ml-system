# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . /app

# Install dependencies
RUN poetry install

# Set the environment variable for the broker address
ENV BROKER_ADDRESS=redpanda-0:9092

# Command to run the application
CMD ["poetry", "run", "python", "services/trade_producer/src/MdProducer.py"]