from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from helpers.signals import post_update
from game.models import Patient, AppliedAction
from template.serializer.state_serialize import StateSerializer

"""
This package is responsible to decide when to notify which consumers.
Events must be sent as strings, thus objects are passed by ids.
Sending events is done by the celery worker.
"""


class ChannelEventTypes:
    ACTION_CONFIRMATION = "action-confirmation"
    ACTION_DECLINATION = "action-declination"
    ACTION_RESULT = "action-result"
    PHASE_UPDATE = "state"


def _notify_group(group_channel_name, event):
    async_to_sync(get_channel_layer().group_send)(group_channel_name, event)


def _notify_instance(instance_channel_name, event):
    async_to_sync(get_channel_layer().send)(instance_channel_name, event)


@receiver(post_update, patient=Patient)
def notify_patient_phase_change(patient):
    state = patient.stateID.get()
    channel = patient.channel_name
    serializer = StateSerializer(state)
    event = {
        "type": ChannelEventTypes.PHASE_UPDATE,
        **serializer.data,
    }
    _notify_group(channel, event)


# ToDO: Update for actual Actions
@receiver(post_save, action=AppliedAction)
def chose_notification_method(action):
    if action.state == AppliedAction.State.DECLINED:
        notify_action_declined(action)
    if action.state == AppliedAction.State.PLANNED:
        notify_action_confirmed(action)


def notify_action_confirmed(action):
    if action.state == AppliedAction.State.DECLINED:
        return
    channel = action.patient.group_name
    event = {
        "messageType": ChannelEventTypes.ACTION_CONFIRMATION,
        "appliedAction": action.id,
    }
    _notify_group(channel, event)


def notify_action_declined(action):
    channel = action.patient.group_name
    event = {
        "messageType": ChannelEventTypes.ACTION_DECLINATION,
        "appliedAction": action.id,
        "actionDeclinationReason": action.reason_of_declination,
    }
    _notify_group(channel, event)
