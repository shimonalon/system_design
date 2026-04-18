"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import get_settings
from src.database import get_db
from src.cache import get_cache
from src.routes import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle (startup and shutdown).
    """
    # Startup
    logger.info("🚀 Starting URL Shortener API...")
    settings = get_settings()

    # Initialize database
    db = get_db()
    db.create_tables()
    logger.info("✅ Database initialized.")

    # Initialize cache
    cache = get_cache(settings.REDIS_URL)
    if not await cache.health_check():
        logger.error("❌ Redis cache is unavailable.")
        raise RuntimeError("Redis cache is unavailable.")
    logger.info("✅ Redis cache initialized.")

    yield

    # Shutdown
    logger.info("🛑 Shutting down URL Shortener API...")
    logger.info("✅ Shutdown complete.")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI instance
    """
    settings = get_settings()
    
    app = FastAPI(
        title="URL Shortener API",
        description="A simple yet scalable URL shortening service",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """
        Health check endpoint.
        """
        return {
            "status": "healthy",
            "version": "1.0.0"
        }

    # Root endpoint
    @app.get("/")
    async def root():
        """
        Root endpoint.
        """
        return {
            "message": "Welcome to URL Shortener API"
        }
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
    )
