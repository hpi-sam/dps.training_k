import logging

from celery import shared_task
from django.conf import settings
from django.db import transaction

from game.models.scheduled_event import ScheduledEvent


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
        if self.request.retries >= self.max_retries:
            logging.error(f"ScheduledEvent {event_id} failed permanently after {self.max_retries} retries: {e}")
            ScheduledEvent.objects.filter(id=event_id).delete()
            return
        logging.error(f"Failed to execute event {event_id}: {e}")
        self.retry(exc=e)

@shared_task
def check_for_updates():
    with transaction.atomic():
        claimed = (
            ScheduledEvent.objects.only('id').select_for_update(skip_locked=True)
            .filter(
                end_date__lte=settings.CURRENT_TIME(),
                enqueued=False
            )
        )
        event_ids = list(claimed.values_list('id', flat=True))
        ScheduledEvent.objects.filter(id__in=event_ids).update(enqueued=True)

    for event_id in event_ids:
        try:
            run_event.apply_async(args=[event_id]) # add event to celery queue for a worker to pick up
        except Exception as e:
            logging.error(f"failed to enqueue event {event_id}: {e}")
