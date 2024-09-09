# Define variables
DOCKER_COMPOSE_FILE = docker-compose.yml

# Start Docker Compose services
start:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop Docker Compose services
stop:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Restart Docker Compose services
restart: stop start

# View logs of Docker Compose services
logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

# Clean up Docker Compose services and remove named volumes
clean:
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v
