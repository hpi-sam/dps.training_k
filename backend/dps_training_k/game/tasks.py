from celery import shared_task
from django.conf import settings
from game.models.scheduled_event import ScheduledEvent


# When this method is changed, the docker container needs to be rebuilt, because the
# Celery-worker doesn't get the update based on our docker configuration
@shared_task
def check_for_updates():
    events = ScheduledEvent.objects.filter(end_date__lte=settings.CURRENT_TIME())
    for event in events:
        event.action()
