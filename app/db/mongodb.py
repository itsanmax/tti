"""
MongoDB connection and helpers.
Uses a single client; FastAPI lifespan connects/disconnects.
"""
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.config import MONGODB_URL, MONGODB_DB_NAME, MONGODB_TRENDS_COLLECTION

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    """Return the shared MongoDB client. Raises if not connected."""
    if _client is None:
        raise RuntimeError("MongoDB client not initialized; call connect_mongodb() on app startup.")
    return _client


def get_database() -> Database:
    """Return the default database."""
    return get_client()[MONGODB_DB_NAME]


def get_trends_collection() -> Collection:
    """Return the collection used for storing Google trends."""
    return get_database()[MONGODB_TRENDS_COLLECTION]


def connect_mongodb() -> MongoClient:
    """Create and store the MongoDB client. Call once on application startup."""
    global _client
    _client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Verify connection
    _client.admin.command("ping")
    return _client


def disconnect_mongodb() -> None:
    """Close the MongoDB client. Call on application shutdown."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
