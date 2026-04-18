# URL Shortener Backend - Makefile

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

# ── Setup ──────────────────────────────────────────────

setup: ## Create virtual environment and install dependencies
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	cp -n .env.example .env || true
	@echo "✅ Setup complete. Edit .env before running."

# ── Run ───────────────────────────────────────────────

run: ## Run the API locally with hot reload
	$(UVICORN) src.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run the API in production mode
	$(UVICORN) src.main:app --host 0.0.0.0 --port 8000 --workers 4

# ── Tests ─────────────────────────────────────────────

test: ## Run all tests
	$(VENV)/bin/pytest tests/ -v

test-unit: ## Run unit tests only
	$(VENV)/bin/pytest tests/test_shortener.py -v

# ── Docker ────────────────────────────────────────────

docker-build: ## Build Docker image
	docker build -t url-shortener-backend .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env url-shortener-backend

# ── Infra ─────────────────────────────────────────────

infra-up: ## Start PostgreSQL and Redis with Docker
	docker run -d --name url_postgres \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=url_shortener \
		-p 5432:5432 postgres:16-alpine
	docker run -d --name url_redis \
		-p 6379:6379 redis:7-alpine
	@echo "✅ PostgreSQL and Redis are running."

infra-down: ## Stop PostgreSQL and Redis
	docker stop url_postgres url_redis
	docker rm url_postgres url_redis

# ── Help ──────────────────────────────────────────────

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
