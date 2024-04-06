from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
import game.models as gm  # needed to avoid circular imports

"""
This package is responsible to decide when to notify which consumers.
Events must be sent as strings, thus objects are passed by ids.
Sending events is done by the celery worker.
"""


class ChannelEventTypes:
    STATE_CHANGE_EVENT = "state.change.event"


def _notify_group(group_channel_name, event):
    async_to_sync(get_channel_layer().group_send)(group_channel_name, event)


def dispatch_patient_event(patient, changes):
    if not changes:
        return
    if "patient_state" in changes:
        notify_patient_state_change(patient)


def notify_patient_state_change(patient):
    channel = get_group_name(patient)
    event = {
        "type": ChannelEventTypes.STATE_CHANGE_EVENT,
    }
    _notify_group(channel, event)


def get_group_name(obj):
    return f"{obj.__class__.__name__}_{obj.id}"


def get_patient_instance(event):
    return gm.Patient.objects.get(pk=event["patientId"])
