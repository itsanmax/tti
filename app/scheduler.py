"""
APScheduler setup for daily jobs.
Runs the Google trends job at 9 AM daily (configurable via TRENDS_JOB_CRON).
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import TRENDS_JOB_CRON
from app.services.trends_service import run_daily_trends_job

logger = logging.getLogger(__name__)
_scheduler: BackgroundScheduler | None = None


def _run_trends_job_sync() -> None:
    """Wrapper for the sync scheduler to call the trends job."""
    try:
        result = run_daily_trends_job()
        logger.info("Daily trends job completed: %s", result)
    except Exception as e:
        logger.exception("Daily trends job failed: %s", e)


def get_scheduler() -> BackgroundScheduler:
    """Return the global scheduler instance; creates it if needed."""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        # Parse cron: "0 9 * * *" = 9 AM every day (minute hour day month day_of_week)
        parts = TRENDS_JOB_CRON.strip().split()
        if len(parts) >= 2:
            minute, hour = int(parts[0]), int(parts[1])
            _scheduler.add_job(
                _run_trends_job_sync,
                CronTrigger(minute=minute, hour=hour, day="*", month="*", day_of_week="*"),
                id="daily_google_trends",
                replace_existing=True,
            )
            logger.info("Scheduled daily trends job at %s:%s (cron: %s)", hour, minute, TRENDS_JOB_CRON)
        else:
            # Fallback: 9 AM
            _scheduler.add_job(
                _run_trends_job_sync,
                CronTrigger(hour=9, minute=0),
                id="daily_google_trends",
                replace_existing=True,
            )
    return _scheduler


def start_scheduler() -> None:
    """Start the background scheduler."""
    get_scheduler().start()
    logger.info("Scheduler started.")


def shutdown_scheduler() -> None:
    """Shutdown the scheduler."""
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("Scheduler stopped.")
