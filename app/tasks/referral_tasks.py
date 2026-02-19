from celery import Celery
from app.core.config import settings
from app.core.database import SessionLocal
from app.services.referral_service import ReferralService
from app.services.reward_service import RewardService
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "referral_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "deactivate-expired-codes": {
            "task": "app.tasks.referral_tasks.deactivate_expired_codes",
            "schedule": 3600.0,
        },
    }
)

@celery_app.task
def deactivate_expired_codes():
    logger.info("Deactivating expired codes")
    db = SessionLocal()
    try:
        service = ReferralService(db)
        count = service.deactivate_expired_codes()
        logger.info(f"Deactivated {count} codes")
        return {"status": "success", "count": count}
    finally:
        db.close()