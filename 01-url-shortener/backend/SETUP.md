# Backend Setup Guide

## Run Locally

### 1. Setup environment
```bash
cd backend
make setup        # Creates venv + installs dependencies + copies .env
```

### 2. Edit `.env`
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/url_shortener
REDIS_URL=redis://localhost:6379/0
BASE_URL=http://localhost:8000
DEBUG=True
CACHE_TTL=86400
```

### 3. Start PostgreSQL and Redis
```bash
make infra-up     # Starts PostgreSQL + Redis in Docker
```

### 4. Run the API
```bash
make run          # Hot reload on http://localhost:8000
```

### Available Commands
```bash
make setup        # Setup virtual environment
make run          # Run locally with hot reload
make run-prod     # Run in production mode
make test         # Run all tests
make test-unit    # Run unit tests only
make infra-up     # Start PostgreSQL + Redis
make infra-down   # Stop PostgreSQL + Redis
make docker-build # Build Docker image
make docker-run   # Run Docker container
```

---

## Deploy to Render.com (Free)

Render connects directly to your GitHub repo and deploys automatically.

### 1. Create a Render account
Go to [https://render.com](https://render.com) and sign up with GitHub.

### 2. Create a new Web Service
- Click **New → Blueprint**
- Connect your GitHub repo
- Render will automatically detect `render.yaml` and set everything up

### 3. Set `BASE_URL` manually
In the Render dashboard, set:
```
BASE_URL=https://your-service-name.onrender.com
```

### 4. Deploy
Every push to `main` will trigger an automatic redeploy. ✅

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/shorten` | Create short URL |
| GET | `/{short_code}` | Redirect to long URL |
| GET | `/api/stats/{short_code}` | Get URL statistics |
| DELETE | `/{short_code}` | Delete short URL |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
