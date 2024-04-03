from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import game.models as gm  # needed to avoid circular imports

"""
This package is responsible to decide when to notify which consumers.
Events must be sent as strings, thus objects are passed by ids.
Sending events is done by the celery worker.
"""


class ChannelEventTypes:
    ACTION_CONFIRMATION_EVENT = "action-confirmation-event"
    ACTION_DECLINATION_EVENT = "action-declination-event"
    ACTION_RESULT_EVENT = "action-result-event"
    STATE_CHANGE_EVENT = "state-change-event"


def _notify_group(group_channel_name, event):
    async_to_sync(get_channel_layer().group_send)(group_channel_name, event)


def _notify_instance(instance_channel_name, event):
    async_to_sync(get_channel_layer().send)(instance_channel_name, event)


def notify_patient_sate_change(patient):
    channel = patient.channel_name
    event = {
        "type": ChannelEventTypes.STATE_CHANGE_EVENT,
        "patientId": patient.id,
    }
    _notify_group(channel, event)


def chose_applied_action_notification_method(applied_action):
    if applied_action.state == gm.AppliedAction.State.DECLINED:
        notify_action_declined(applied_action)
    if applied_action.state == gm.AppliedAction.State.PLANNED:
        notify_action_confirmed(applied_action)
    if applied_action.state == gm.AppliedAction.State.FINISHED:
        applied_action.patient.action_finished()
        notify_action_result(applied_action)


def notify_action_confirmed(applied_action):
    channel = applied_action.patient.group_name
    event = {
        "type": ChannelEventTypes.ACTION_CONFIRMATION_EVENT,
        "actionId": applied_action.id,
    }
    _notify_group(channel, event)


def notify_action_declined(applied_action):
    channel = applied_action.patient.group_name
    event = {
        "type": ChannelEventTypes.ACTION_DECLINATION_EVENT,
        "actionId": applied_action.id,
    }
    _notify_group(channel, event)


def notify_action_result(applied_action):
    channel = applied_action.patient.group_name
    event = {
        "type": ChannelEventTypes.ACTION_RESULT_EVENT,
        "actionId": applied_action.id,
    }
    _notify_group(channel, event)


# decode events without context knowledge outside this package
def get_applied_action_instance(event):
    return gm.AppliedAction.objects.get(pk=event["actionId"])


def get_patient_instance(event):
    return gm.Patient.objects.get(pk=event["patientId"])
