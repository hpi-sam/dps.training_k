from celery import shared_task
from django.conf import settings
from game.models.scheduled_event import ScheduledEvent


@shared_task
def check_for_updates():
    events = ScheduledEvent.objects.filter(date__lte=settings.CURRENT_TIME())
    for event in events:
        event.action()
        return True
