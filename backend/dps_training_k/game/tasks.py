from celery import shared_task
from django.conf import settings
from game.models.scheduled_event import ScheduledEvent
import logging
import uuid
from django.db import transaction

# When any of these methods is changed, the docker container needs to be rebuilt, because the
# Celery-worker doesn't get the update with our docker configuration

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def run_event(self, event_id):
    try:
        event = ScheduledEvent.objects.get(id=event_id)
        event.action()
    except ScheduledEvent.DoesNotExist:
        logging.warning(f"ScheduledEvent {event_id} already deleted.")
    except Exception as e:
        logging.error(f"Failed to execute event {event_id}: {e}")
        self.retry(exc=e)

@shared_task
def check_for_updates():
    worker_id = str(uuid.uuid4())
    with transaction.atomic(): # atomic db operation
        claimed = (
            ScheduledEvent.objects.only('id').select_for_update(skip_locked=True) # locks selected rows, skips already locked ones
            .filter(
                end_date__lte=settings.CURRENT_TIME(),
                locked_by__isnull=True
            )
        )
        event_ids = list(claimed.values_list('id', flat=True))
        ScheduledEvent.objects.filter(id__in=event_ids).update(
            locked_by=worker_id
        ) # mark events as claimed by worker

    for event_id in event_ids:
        try:
            run_event.apply_async(args=[event_id]) # add event to celery queue for a worker to pick up
        except Exception as e:
            logging.error(f"failed to enqueue event {event_id}: {e}")
