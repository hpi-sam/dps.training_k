from celery import shared_task
from django.conf import settings
from game.models.scheduled_event import ScheduledEvent
from redis import Redis
from redis.exceptions import LockError
import logging

redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# When this method is changed, the docker container needs to be rebuilt, because the
# Celery-worker doesn't get the update based on our docker configuration
@shared_task
def check_for_updates():
    lock_id = 'check_for_updates_lock'
    lock = redis_client.lock(lock_id)

    try:
        if lock.acquire(blocking=False):
            try:
                events = ScheduledEvent.objects.filter(end_date__lte=settings.CURRENT_TIME())
                for event in events:
                    event.action()
            finally:
                lock.release()
        else:
            logging.info("Task is already running")
    except LockError as e:
        logging.warning(f"Could not acquire lock: {e}")
