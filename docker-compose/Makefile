# Define variables
DOCKER_COMPOSE_FILE = docker-compose.yml

# Start Docker Compose services
start-redpanda:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop Docker Compose services
stop-redpanda:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Restart Docker Compose services
restart-redpanda: stop-redpanda start-redpanda

# View logs of Docker Compose services
logs-redpanda:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f

# Clean up Docker Compose services and remove named volumes
clean-redpanda:
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v

# Start feature pipeline
start-feature-pipeline:
	docker compose -f feature-pipeline.yml up --build -d

# Stop feature pipeline
stop-feature-pipeline:
	docker compose -f feature-pipeline.yml down

# Restart feature pipeline
restart-feature-pipeline: stop-feature-pipeline start-feature-pipeline

# View logs of feature pipeline
logs-feature-pipeline:
	docker compose -f feature-pipeline.yml logs -f
