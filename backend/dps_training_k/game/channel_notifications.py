import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import game.models as models  # needed to avoid circular imports

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
    ACTION_RESULT_EVENT = "action.result.event"
    ACTION_LIST_EVENT = "action.list.event"
    MATERIAL_CHANGE_EVENT = "material.change.event"


class ChannelNotifier:
    @classmethod
    # If used in overwritten save method, it must be called before any calls to super().save
    def save_and_notify(cls, obj, changes, save_origin, *args, **kwargs):
        is_updated = not obj._state.adding
        if is_updated and not changes:
            message = f"""{obj.__class__.__name__} have to be saved with save(update_fields=[...]) after initial creation.
           This is to ensure that the frontend is notified of changes."""
            logging.warning(message)

        save_origin.save(*args, **kwargs)
        cls.dispatch_event(obj, changes)

    @classmethod
    def delete_and_notify(cls, obj, changes):
        raise NotImplementedError(
            "Method delete_and_notify must be implemented by subclass"
        )

    @classmethod
    def _notify_group(cls, group_channel_name, event):
        """
        Handled internally by the channels dispatcher. Will try to call a method with event.type as name at the receiver; "." are replaced by "_".
        For more info look into:
        https://channels.readthedocs.io/en/stable/topics/channel_layers.html?highlight=periods#what-to-send-over-the-channel-layer
        """
        async_to_sync(get_channel_layer().group_send)(group_channel_name, event)

    @classmethod
    def get_group_name(cls, obj):
        return f"{obj.__class__.__name__}_{obj.id}"

    @classmethod
    def dispatch_event(cls, obj, changes):
        raise NotImplementedError(
            "Method dispatch_event must be implemented by subclass"
        )

    @classmethod
    def _notify_exercise_update(cls, exercise):
        channel = cls.get_group_name(exercise)
        event = {
            "type": ChannelEventTypes.EXERCISE_UPDATE,
            "exercise_pk": exercise.id,
        }
        cls._notify_group(channel, event)


class PatientInstanceDispatcher(ChannelNotifier):

    @classmethod
    def dispatch_event(cls, patient_instance, changes):
        if changes is not None and "patient_state" in changes:
            cls._notify_patient_state_change(patient_instance)

        if not (changes is not None and len(changes) == 1 and "patient_state"):
            cls._notify_exercise_update(patient_instance.exercise)

    @classmethod
    def _notify_patient_state_change(cls, patient_instance):
        channel = cls.get_group_name(patient_instance)
        event = {
            "type": ChannelEventTypes.STATE_CHANGE_EVENT,
            "patient_instance_pk": patient_instance.id,
        }
        cls._notify_group(channel, event)

    @classmethod
    def delete_and_notify(cls, patient, *args, **kwargs):
        exercise = patient.exercise
        super(patient.__class__, patient).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)


class AreaDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, area, changes):
        cls._notify_exercise_update(area.exercise)

    @classmethod
    def delete_and_notify(cls, area, *args, **kwargs):
        exercise = area.exercise
        super(area.__class__, area).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)


class PersonnelDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, personnel, changes):
        cls._notify_exercise_update(personnel.area.exercise)

    @classmethod
    def delete_and_notify(cls, personnel, *args, **kwargs):
        exercise = personnel.area.exercise
        super(personnel.__class__, personnel).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)


class QueueDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, obj, changes):
        cls._notify_queue_change(obj)

    @classmethod
    def _notify_queue_change(cls, obj):
        for entity in [obj.get_action_instance.patient_instance, obj.get_action_instance.lab, obj.]:#hier blöd weil mehrfachbenachrichtigung durch produktionsaktionen
        channel = cls.get_group_name(obj.get_)
        event = {
            "type": ChannelEventTypes.ACTION_LIST_EVENT,
            "queue_entry": obj.id,
        }
        cls._notify_group(channel, event)


class ActionInstanceDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, obj, changes):
        applied_action = obj
        if changes and not ("current_state" in changes):
            raise ValueError(
                "There has to be a state change or order id change whenever updating an ActionInstance."
            )
        # state change events

        event_type = {
            models.ActionInstanceStateNames.PLANNED: ChannelEventTypes.ACTION_CONFIRMATION_EVENT,
            models.ActionInstanceStateNames.FINISHED: ChannelEventTypes.ACTION_RESULT_EVENT,
        }.get(applied_action.state_name)
        cls._notify_action_event(
            event_type, applied_action, ChannelEventTypes.ACTION_CONFIRMATION_EVENT
        )

        # always send action list event
        cls._notify_action_event(applied_action, ChannelEventTypes.ACTION_LIST_EVENT)


class PatientActionInstanceDispatcher(ActionInstanceDispatcher):
    @classmethod
    def _notify_action_event(cls, action_instance, event_type):
        channel = cls.get_group_name(action_instance.patient_instance)
        event = {
            "type": event_type,
            "action_instance_pk": action_instance.id,
            "action_instance_class": "PatientActionInstance",
        }
        cls._notify_group(channel, event)


class LabActionInstanceDispatcher(ActionInstanceDispatcher):
    @classmethod
    def _notify_action_event(cls, action_instance, event_type):
        channel = cls.get_group_name(action_instance.lab)
        event = {
            "type": event_type,
            "action_instance_pk": action_instance.id,
            "action_instance_class": "LabActionInstance",
        }
        cls._notify_group(channel, event)


class InventoryEntryDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, obj, changes):
        cls.notify_material_change_event(obj)

    @classmethod
    def notify_material_change_event(cls, inventory_entry):
        channel = cls.get_group_name(inventory_entry.inventory.get_owner())
        event = {
            "type": ChannelEventTypes.MATERIAL_CHANGE_EVENT,
            "inventory_entry_pk": inventory_entry.id,
        }
        cls._notify_group(channel, event)
