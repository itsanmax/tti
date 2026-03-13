"""
Application config and constants.
Use environment variables for secrets; see .env.example.
"""
import os
from typing import Optional

# ----- MongoDB -----
MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "tti")
MONGODB_TRENDS_COLLECTION: str = os.getenv("MONGODB_TRENDS_COLLECTION", "google_trends")

# ----- Scheduler (9 AM daily, server local time) -----
TRENDS_JOB_CRON: str = os.getenv("TRENDS_JOB_CRON", "0 9 * * *")  # minute hour day month weekday
TRENDS_TOP_N: int = int(os.getenv("TRENDS_TOP_N", "5"))
TRENDS_COUNTRY: str = os.getenv("TRENDS_COUNTRY", "united_states")  # pytrends country code

# ----- Optional URLs (for future APIs) -----
# API_BASE_URL: Optional[str] = os.getenv("API_BASE_URL")
