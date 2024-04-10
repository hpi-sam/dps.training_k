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
    ACTION_CONFIRMATION_EVENT = "action.confirmation.event"
    ACTION_DECLINATION_EVENT = "action.declination.event"
    ACTION_RESULT_EVENT = "action.result.event"


class ChannelNotifier:
    @classmethod
    def save_and_notify(cls, obj, update_fields, *args, **kwargs):
        is_updated = not obj._state.adding
        if is_updated and not update_fields:
            message = """AppliedActions have to be saved with save(update_fields=[...]) after initial creation. 
            This is to ensure that the frontend is notified of changes."""
            raise Exception(message)

        super(obj.__class__, obj).save(*args, **kwargs)
        cls.dispatch_event(obj, update_fields)

    @classmethod
    def _notify_group(cls, group_channel_name, event):
        async_to_sync(get_channel_layer().group_send)(group_channel_name, event)

    @classmethod
    def get_group_name(cls, obj):
        return f"{obj.__class__.__name__}_{obj.id}"

    @classmethod
    def dispatch_event(cls, obj, changes):
        raise NotImplementedError(
            "Method dispatch_event must be implemented by subclass"
        )


class PatientDispatcher(ChannelNotifier):

    @classmethod
    def dispatch_event(cls, patient, changes):
        if not changes:
            return
        if "patient_state" in changes:
            cls._notify_patient_state_change(patient)

    @classmethod
    def _notify_patient_state_change(cls, patient):
        channel = cls.get_group_name(patient)
        event = {
            "type": ChannelEventTypes.STATE_CHANGE_EVENT,
        }
        cls._notify_group(channel, event)


def get_group_name(obj):
    return f"{obj.__class__.__name__}_{obj.id}"


def get_patient_instance(event):
    return gm.Patient.objects.get(pk=event["patientId"])
