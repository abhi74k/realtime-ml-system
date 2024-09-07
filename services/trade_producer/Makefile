# Define variables
IMAGE_NAME = trade_producer_image
CONTAINER_NAME = trade_producer_container
BROKER_ADDRESS = redpanda-0:9092

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .
	
# Run the Docker container
run: clean build
	docker run --name $(CONTAINER_NAME) --network redpanda_network $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)

# Clean up the Docker container
clean:
	docker rm -f $(CONTAINER_NAME)

# Rebuild and run the Docker container
rebuild: clean run