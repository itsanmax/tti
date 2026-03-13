"""
API endpoints for Google trends job and stored trends.
"""
from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from app.db.mongodb import get_trends_collection
from app.services.trends_service import run_daily_trends_job

router = APIRouter()


@router.post("/trends/run-job")
async def trigger_trends_job():
    """
    Manually trigger the daily trends job (fetch top 5 from Google, store in MongoDB).
    """
    try:
        result = run_daily_trends_job()
        return {"ok": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/latest")
async def get_latest_trends(limit: int = 10):
    """
    Return the most recently stored trends (by created_at).
    """
    try:
        coll = get_trends_collection()
        cursor = coll.find().sort("created_at", -1).limit(limit)
        items = list(cursor)
        # Convert ObjectId and datetime for JSON
        for doc in items:
            doc["_id"] = str(doc["_id"])
            if hasattr(doc.get("created_at"), "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
        return {"count": len(items), "trends": items}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))
