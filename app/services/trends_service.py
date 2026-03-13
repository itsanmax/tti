"""
Service to fetch top Google trends and store them in MongoDB.
Designed to be run daily (e.g. 9 AM) via scheduler.
"""
import logging
from datetime import datetime, timezone
from typing import List

from app.config import TRENDS_TOP_N, TRENDS_COUNTRY
from app.db.mongodb import get_trends_collection

logger = logging.getLogger(__name__)


def fetch_top_google_trends(count: int = TRENDS_TOP_N, country: str = TRENDS_COUNTRY) -> List[str]:
    """
    Fetch top trending search terms from Google Trends for the given country.
    Returns a list of trend strings (up to `count`).
    """
    try:
        from pytrends.request import TrendReq
    except ImportError:
        logger.error("pytrends not installed; pip install pytrends")
        return []

    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        # trending_searches returns list of strings for the region
        trending = pytrends.trending_searches(pn=country)
        if trending is None or not len(trending):
            return []
        # pytrends returns DataFrame (1 col) or list
        if hasattr(trending, "iloc"):
            items = trending.iloc[:count, 0].tolist()
        else:
            items = list(trending)[:count]
        return [str(x).strip() for x in items if x is not None and str(x).strip()][:count]
    except Exception as e:
        logger.exception("Failed to fetch Google trends: %s", e)
        return []


def store_trends_in_mongodb(trends: List[str]) -> int:
    """
    Store a list of trend keywords into the MongoDB trends collection.
    Each document: keyword, rank (1-based), date (day), source, created_at.
    Returns the number of documents inserted.
    """
    if not trends:
        return 0
    coll = get_trends_collection()
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    docs = [
        {
            "keyword": kw,
            "rank": i + 1,
            "date": date_str,
            "source": "google_trends",
            "created_at": now,
        }
        for i, kw in enumerate(trends)
    ]
    result = coll.insert_many(docs)
    logger.info("Stored %d trends for date %s", len(result.inserted_ids), date_str)
    return len(result.inserted_ids)


def run_daily_trends_job() -> dict:
    """
    Run the full job: fetch top N Google trends and store in MongoDB.
    Returns a small summary dict for logging/API.
    """
    trends = fetch_top_google_trends(count=TRENDS_TOP_N, country=TRENDS_COUNTRY)
    inserted = store_trends_in_mongodb(trends)
    return {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "fetched": len(trends),
        "stored": inserted,
        "trends": trends,
    }
