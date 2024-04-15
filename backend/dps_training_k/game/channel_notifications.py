from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import game.models as models
import logging

"""
This package is responsible to decide when to notify which consumers.
This also implies that it should be as transparent as possible to the models it watches.
Events must be sent as strings, thus objects are passed by ids.
Sending events is done by the celery worker.
"""


class ChannelEventTypes:
    STATE_CHANGE_EVENT = "state.change.event"
    EXERCISE_UPDATE = "send.exercise.event"
    ACTION_CONFIRMATION_EVENT = "action.confirmation.event"
    ACTION_DECLINATION_EVENT = "action.declination.event"
    ACTION_RESULT_EVENT = "action.result.event"


class ChannelNotifier:
    @classmethod
    # If used in overwritten save method, it must be called before any calls to super().save
    def save_and_notify(cls, obj, changes, *args, **kwargs):
        is_updated = not obj._state.adding
        if is_updated and not changes:
            message = f"""{cls.__name} have to be saved with save(update_fields=[...]) after initial creation. 
            This is to ensure that the frontend is notified of changes."""
            logging.warning(message)

        super(obj.__class__, obj).save(*args, **kwargs)
        cls.dispatch_event(obj, changes)

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


class AreaDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, area, changes):
        cls._notify_exercise_update(area.exercise)

    @classmethod
    def _notify_exercise_update(cls, exercise):
        channel = cls.get_group_name(exercise)
        event = {
            "type": ChannelEventTypes.EXERCISE_UPDATE,
            "exercise_pk": exercise.id,
        }
        cls._notify_group(channel, event)


class ActionInstanceDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, obj, changes):
        applied_action = obj
        if changes and not "state" in changes:
            raise ValueError(
                "There has to be a state change whenever updating an ActionInstance."
            )
        if applied_action.state_name == models.ActionInstanceStateNames.DECLINED:
            event_type = ChannelEventTypes.ACTION_DECLINATION_EVENT
        elif applied_action.state_name == models.ActionInstanceStateNames.PLANNED:
            event_type = ChannelEventTypes.ACTION_CONFIRMATION_EVENT
        elif applied_action.state_name == models.ActionInstanceStateNames.FINISHED:
            event_type = ChannelEventTypes.ACTION_RESULT_EVENT
        else:
            return
        cls._notify_action_event(applied_action, event_type)

    @classmethod
    def _notify_action_event(cls, applied_action, event_type):
        channel = cls.get_group_name(applied_action.patient)
        event = {
            "type": event_type,
            "action_pk": applied_action.id,
        }
        cls._notify_group(channel, event)
