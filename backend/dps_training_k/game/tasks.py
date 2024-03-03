from celery import shared_task
from django.utils import timezone
from game.models.scheduled_event import ScheduledEvent


@shared_task
def check_for_updates():
    events = ScheduledEvent.objects.filter(date__lte=timezone.now()).order_by("date")
    for event in events:
        event.action()
