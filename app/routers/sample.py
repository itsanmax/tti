"""
Sample API router - add more routers in this package as needed.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello():
    """Sample GET endpoint."""
    return {"message": "Hello from TTI API"}


@router.get("/items/{item_id}")
async def get_item(item_id: int, q: str | None = None):
    """Sample path and query parameter endpoint."""
    return {"item_id": item_id, "q": q}

"""
Google Trends API:
- https://trends.google.com/trends/api/explore/trendingsearches/daily?geo=IN
- https://trends.google.com/trends/api/explore/trendingsearches/daily?geo=IN&category=0&N=10


TODO: Add below routes:
- api/v1/getlatesttrends (Get latest trends from the Google Trends)
- api/v1/getlatesttrendingtopics (Get latest trending topics from the Google Trends)
- api/v1/getlatesttrendingtopics
"""