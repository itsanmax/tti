"""
TTI FastAPI application entry point.
"""
from fastapi import FastAPI

from app.routers import sample

app = FastAPI(
    title="TTI API",
    description="Text to Image - API service",
    version="0.1.0",
)

# Include routers
app.include_router(sample.router, prefix="/api/v1", tags=["sample"])


@app.get("/")
async def root():
    """Health / root endpoint."""
    return {"service": "TTI API", "status": "ok"}


@app.get("/health")
async def health():
    """Health check for load balancers / monitoring."""
    return {"status": "healthy"}

