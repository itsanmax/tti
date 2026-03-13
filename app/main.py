"""
TTI FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.mongodb import connect_mongodb, disconnect_mongodb
from app.routers import sample, trends
from app.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect MongoDB and start scheduler on startup; disconnect and stop on shutdown."""
    connect_mongodb()
    start_scheduler()
    yield
    shutdown_scheduler()
    disconnect_mongodb()


app = FastAPI(
    title="TTI API",
    description="Text to Image - API service",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(sample.router, prefix="/api/v1", tags=["sample"])
app.include_router(trends.router, prefix="/api/v1", tags=["trends"])


@app.get("/")
async def root():
    """Health / root endpoint."""
    return {"service": "TTI API", "status": "ok"}


@app.get("/health")
async def health():
    """Health check for load balancers / monitoring."""
    return {"status": "healthy"}
