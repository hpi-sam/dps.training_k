from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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


def _notify_instance(instance_channel_name, event):
    async_to_sync(get_channel_layer().send)(instance_channel_name, event)


def dispatch_patient_event(patient, changes):
    if "patient_state" in changes:
        notify_patient_state_change(get_patient_instance(patient))


def notify_patient_state_change(patient):
    channel = patient.channel_name
    event = {
        "type": ChannelEventTypes.STATE_CHANGE_EVENT,
    }
    _notify_group(channel, event)


def get_patient_instance(event):
    return gm.Patient.objects.get(pk=event["patientId"])
