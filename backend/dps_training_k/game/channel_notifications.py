from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from helpers.signals import post_update
from game.models import Patient
from template.serializer.state_serialize import StateSerializer


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
