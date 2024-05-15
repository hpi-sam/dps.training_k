import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import game.models as models  # needed to avoid circular imports
import template.models as template

"""
This package is responsible to decide when to notify which consumers.
This also implies that it should be as transparent as possible to the models it watches.
Events must be sent as strings, thus objects are passed by ids.
Sending events is done by the celery worker.
"""


class ChannelEventTypes:
    STATE_CHANGE_EVENT = "state.change.event"
    EXERCISE_UPDATE = "send.exercise.event"
    EXERCISE_START_EVENT = "exercise.start.event"
    EXERCISE_END_EVENT = "exercise.end.event"
    ACTION_CONFIRMATION_EVENT = "action.confirmation.event"
    ACTION_LIST_EVENT = "action.list.event"
    LOG_UPDATE_EVENT = "log.update.event"


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
        cls.dispatch_event(obj, changes, is_updated)
        cls.create_trainer_log(obj, changes, is_updated)

    @classmethod
    def delete_and_notify(cls, obj, changes):
        raise NotImplementedError(
            "Method delete_and_notify must be implemented by subclass"
        )

    @classmethod
    def _notify_group(cls, group_channel_name, event):
        """
        Handled internally by the channels' dispatcher. Will try to call a method with event.type as name at the receiver; "." are replaced by "_".
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
    def create_trainer_log(cls, obj, changes, is_updated):
        pass

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
    def dispatch_event(cls, obj, changes, is_updated):
        applied_action = obj
        if changes and not ("current_state" in changes or "order_id" in changes):
            raise ValueError(
                "There has to be a state change or order id change whenever updating an ActionInstance."
            )
        # state change events
        if changes:
            if "current_state" in changes:
                if applied_action.state_name == models.ActionInstanceStateNames.PLANNED:
                    cls._notify_action_event(
                        applied_action, ChannelEventTypes.ACTION_CONFIRMATION_EVENT
                    )

            # always send action list event
            cls._notify_action_event(
                applied_action, ChannelEventTypes.ACTION_LIST_EVENT
            )

    @classmethod
    def _notify_action_event(cls, applied_action, event_type):
        if not applied_action.patient_instance and not applied_action.lab:
            raise ValueError(
                "ActionInstance must be associated with a patient_instance or lab."
            )
        if applied_action.patient_instance:
            channel = cls.get_group_name(applied_action.patient_instance)
        if applied_action.lab:
            channel = cls.get_group_name(applied_action.lab)

        event = {
            "type": event_type,
            "action_instance_pk": applied_action.id,
        }
        cls._notify_group(channel, event)

    @classmethod
    def create_trainer_log(cls, applied_action, changes, is_updated):
        if applied_action == models.ActionInstanceStateNames.PLANNED:
            return

        message = None
        if applied_action.state_name == models.ActionInstanceStateNames.IN_PROGRESS:
            message = f'"{applied_action.name}" wurde gestartet'
        elif applied_action.state_name == models.ActionInstanceStateNames.FINISHED:
            message = f'"{applied_action.name}" wurde abgeschlossen'
            if (
                applied_action.action_template.category
                == template.Action.Category.PRODUCTION
            ):
                named_produced_resources = {
                    material.name: amount
                    for material, amount in applied_action.action_template.produced_resources().items()
                }
                message += f" und hat {str(named_produced_resources)} produziert"
        elif (
            applied_action.state_name == models.ActionInstanceStateNames.CANCELED
            and applied_action.states.filter(
                name=models.ActionInstanceStateNames.IN_PROGRESS
            ).exists()
        ):
            message = f'"{applied_action.name}" wurde abgebrochen'
        elif applied_action.state_name == models.ActionInstanceStateNames.IN_EFFECT:
            message = f'"{applied_action.name}" beginnt zu wirken'
        elif applied_action.state_name == models.ActionInstanceStateNames.EXPIRED:
            message = f'"{applied_action.name}" wirkt nicht mehr'

        if message:
            log_entry = models.LogEntry.objects.create(
                exercise=applied_action.exercise,
                message=message,
                patient_instance=applied_action.patient_instance,
                area=applied_action.area,
                is_dirty=True,
            )
            personnel_list = models.Personnel.objects.filter(
                action_instance=applied_action
            )
            log_entry.personnel.add(*personnel_list)
            material_list = models.MaterialInstance.objects.filter(
                patient_instance=applied_action.patient_instance,
                lab=applied_action.lab,
            )
            log_entry.materials.add(*material_list)
            log_entry.is_dirty = False
            log_entry.save(update_fields=["is_dirty"])


class AreaDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, area, changes, is_updated):
        cls._notify_exercise_update(area.exercise)

    @classmethod
    def delete_and_notify(cls, area, *args, **kwargs):
        exercise = area.exercise
        super(area.__class__, area).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)


class ExerciseDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, obj, changes, is_updated):
        if changes and "state" in changes:
            if obj.state == models.Exercise.StateTypes.RUNNING:
                cls._notify_exercise_start_event(obj)
            if obj.state == models.Exercise.StateTypes.FINISHED:
                cls._notify_exercise_end_event(obj)

    @classmethod
    def create_trainer_log(cls, exercise, changes, is_updated):
        if not is_updated:
            return
        message = ""
        if (
            changes
            and "state" in changes
            and exercise.state == models.Exercise.StateTypes.RUNNING
        ):
            message = "Übung gestartet"
        if message:
            models.LogEntry.objects.create(exercise=exercise, message=message)

    @classmethod
    def _notify_exercise_start_event(cls, exercise):
        channel = cls.get_group_name(exercise)
        event = {"type": ChannelEventTypes.EXERCISE_START_EVENT}
        cls._notify_group(channel, event)

    @classmethod
    def _notify_exercise_end_event(cls, exercise):
        channel = cls.get_group_name(exercise)
        event = {"type": ChannelEventTypes.EXERCISE_END_EVENT}
        cls._notify_group(channel, event)


class MaterialInstanceDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, material, changes, is_updated):
        cls._notify_exercise_update(material.attached_instance().exercise)

    @classmethod
    def delete_and_notify(cls, material, *args, **kwargs):
        exercise = material.attached_instance().exercise
        super(material.__class__, material).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)


class LogEntryDispatcher(ChannelNotifier):
    @classmethod
    def get_group_name(cls, exercise):
        return f"{exercise.__class__.__name__}_{exercise.id}_log"

    @classmethod
    def dispatch_event(cls, log_entry, changes, is_updated):
        if log_entry.is_valid():
            cls._notify_log_update_event(log_entry)

    @classmethod
    def _notify_log_update_event(cls, log_entry):
        channel = cls.get_group_name(log_entry.exercise)
        event = {
            "type": ChannelEventTypes.LOG_UPDATE_EVENT,
            "log_entry_pk": log_entry.id,
        }
        cls._notify_group(channel, event)


class PatientInstanceDispatcher(ChannelNotifier):

    @classmethod
    def dispatch_event(cls, patient_instance, changes, is_updated):
        if changes is not None and "patient_state" in changes:
            cls._notify_patient_state_change(patient_instance)

        if not (changes is not None and len(changes) == 1 and "patient_state"):
            cls._notify_exercise_update(patient_instance.exercise)

    @classmethod
    def create_trainer_log(cls, patient_instance, changes, is_updated):
        message = None
        if not is_updated:
            message = f"Patient*in {patient_instance.name}({patient_instance.code}) wurde eingeliefert."
            if (
                patient_instance.static_information
                and patient_instance.static_information.injury
            ):
                message += f" Patient*in hat folgende Verletzungen: {patient_instance.static_information.injury}"
        elif "triage" in changes:
            message = f"Patient*in {patient_instance.name} wurde triagiert auf {patient_instance.triage.label}"
        if message:
            models.LogEntry.objects.create(
                exercise=patient_instance.exercise,
                message=message,
                patient_instance=patient_instance,
            )

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


class PersonnelDispatcher(ChannelNotifier):
    @classmethod
    def dispatch_event(cls, personnel, changes, is_updated):
        cls._notify_exercise_update(personnel.area.exercise)

    @classmethod
    def delete_and_notify(cls, personnel, *args, **kwargs):
        exercise = personnel.area.exercise
        super(personnel.__class__, personnel).delete(*args, **kwargs)
        cls._notify_exercise_update(exercise)
