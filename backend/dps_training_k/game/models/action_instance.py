from abc import abstractmethod

from django.db import models

from game.channel_notifications import (
    PatientActionInstanceDispatcher,
    LabActionInstanceDispatcher,
)
from game.models import ScheduledEvent
from helpers.local_timable import LocalTimeable
from helpers.one_field_not_null import one_or_more_field_not_null


class ActionInstanceStateNames(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    ON_HOLD = "OH", "on_hold"
    FINISHED = "FI", "finished"
    IN_EFFECT = "IE", "in effect"
    EXPIRED = "EX", "expired"
    CANCELED = "CA", "canceled"


class ActionInstanceState(models.Model):
    """
    State switching & information logic for ActionInstance
    """

    patient_action_instance = models.ForeignKey(
        "PatientActionInstance",
        on_delete=models.CASCADE,
        related_name="states",
        null=True,
    )
    lab_action_instance = models.ForeignKey(
        "LabActionInstance",
        on_delete=models.CASCADE,
        related_name="states",
        null=True,
    )

    @property
    def action_instance(self):
        if self.patient_action_instance:
            return self.patient_action_instance
        return self.lab_action_instance

    name = models.CharField(choices=ActionInstanceStateNames.choices, max_length=2)
    t_local_begin = models.IntegerField()
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )
    info_text = models.CharField(null=True, blank=True, default=None)

    def update(self, state_name, time, info_text=None):
        if state_name == self.name and not info_text:
            return None
        if state_name == self.name and info_text:
            self.add_info(info_text)
            return None
        self.t_local_end = time
        self.save(update_fields=["t_local_end"])
        new_state = ActionInstanceState.objects.create(
            name=state_name,
            t_local_begin=time,
            info_text=info_text,
        )
        new_state.set_action_instance_type(self.action_instance)
        return new_state

    def add_info(self, info_text):
        self.info_text = self.info_text + info_text
        self.save(update_fields=["info_text"])

    def set_action_instance_type(self, action_instance):
        if isinstance(action_instance, PatientActionInstance):
            self.patient_action_instance = action_instance
            self.save(update_fields=["patient_action_instance"])

        elif isinstance(action_instance, LabActionInstance):
            self.lab_action_instance = action_instance
            self.save(update_fields=["lab_action_instance"])
        else:
            raise ValueError("ActionInstance type not recognized")

    @classmethod
    def success_states():
        return [ActionInstanceStateNames.FINISHED, ActionInstanceStateNames.IN_EFFECT]

    @classmethod
    def completion_states():
        return [ActionInstanceStateNames.FINISHED, ActionInstanceStateNames.EXPIRED]


class Queue(models.Model):
    class Meta:
        ordering = ["order_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["order_id", "patient_instance"],
                name="unique_order_id_for_patient",
            )
        ]

    order_id = models.IntegerField()
    patient_instance = models.ForeignKey("PatientInstance", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.order_id is None:
            self.order_id = self._generate_order_id(self.patient_instance)
        super().save(*args, **kwargs)

    def _generate_order_id(self, patient_instance):
        # Use aggregate to find the maximum order_id for the specified patient_instance
        result = Queue.objects.filter(patient_instance=patient_instance).aggregate(
            max_order_id=models.Max("order_id")
        )
        max_order_id = result["max_order_id"]
        if max_order_id is None:
            new_order_id = 0
        else:
            new_order_id = max_order_id + 1
        return new_order_id

    def get_action_instance(self):
        if LabActionInstance.objects.filter(queue=self).exists():
            return self.lab_action_instance
        if PatientActionInstance.objects.filter(queue=self).exists():
            return self.patient_action_instance
        raise ValueError("No ActionInstance found for queue Entry")


class ActionInstance(LocalTimeable, models.Model):
    """
    Behaviour Strategy for ActionInstances. Should be expanded by subclasses. Triggers State changes.
    """

    class Meta:
        abstract = True

    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, blank=True, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, blank=True, null=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, blank=True, null=True)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    current_state = models.ForeignKey(
        "ActionInstanceState", on_delete=models.CASCADE, blank=True, null=True
    )
    queue = models.OneToOneField(
        "Queue", on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def name(self):
        return self.action_template.name

    @property
    def state_name(self):
        if self.current_state != None:
            return self.current_state.name
        else:
            return None

    @property
    def result(self):
        if (
            self.current_state != None
            and self.current_state.name in ActionInstanceState.success_states()
        ):
            return self.states.get(name=ActionInstanceStateNames.FINISHED).info_text
        else:
            return None

    @property
    def completed(self):
        if self.current_state in ActionInstanceState.completion_states():
            return True
        else:
            return False

    def _update_state(self, state_name, info_text=None):
        new_state = self.current_state.update(
            state_name, self.get_local_time(), info_text
        )
        if new_state:
            self.current_state = new_state
            self.save(update_fields=["current_state"])
        return self.current_state

    @classmethod
    def create(
        cls,
        action_template,
        place_of_application,
        patient_instance=None,
        area=None,
        lab=None,
    ):
        if not patient_instance and not area:
            raise ValueError(
                "Either patient_instance, area or lab must be provided - an action instance always need a context"
            )

        action_instance = cls.objects.create(
            action_template=action_template,
            patient_instance=patient_instance,
            area=area,
            lab=lab,
            queue=Queue.objects.create(patient_instance=patient_instance),
        )
        action_instance.current_state = ActionInstanceState.objects.create(
            name=ActionInstanceStateNames.PLANNED,
            t_local_begin=action_instance.get_local_time(),
        )
        place_of_application.register_to_queue(action_instance)
        action_instance.current_state.set_action_instance_type(action_instance)
        action_instance.save(update_fields=["current_state"])
        return action_instance

    def try_application(self):
        is_applicable, context = self._check_application_status()
        if not is_applicable:
            self._update_state(ActionInstanceStateNames.ON_HOLD, context)
            return False

        self._start_application()
        return True

    def _start_application(self):
        self._create_scheduled_event(
            self.action_template.application_duration, "_application_finished"
        )
        self._consume_resources()
        self._update_state(ActionInstanceStateNames.IN_PROGRESS)

    def _application_finished(self, patient_state):
        self._update_state(
            ActionInstanceStateNames.FINISHED,
            info_text=self.action_template.get_result(patient_state),
        )
        self._application_finished_strategy()

    @abstractmethod
    def _consume_resources(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _application_finished_strategy(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethodLabActionInstance
    @abstractmethod
    def _check_application_status(self):
        raise NotImplementedError("Subclasses must implement this method")


class PatientActionInstance(ActionInstance):

    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True
    )

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        PatientActionInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    @classmethod
    def create(cls, action_template, patient_instance, area=None):
        obj = super().create(
            action_template,
            place_of_application=patient_instance.area,
            area=area,
            patient_instance=patient_instance,
        )
        return obj

    def _check_application_status(self):
        return self.action_template.application_status(
            self.patient_instance, self.patient_instance.area
        )

    def _create_scheduled_event(self, duration, scheduled_method):
        return ScheduledEvent.create_event(
            self.patient_instance.exercise,
            duration,  # ToDo: Replace with scalable local time system
            scheduled_method,
            patient_action_instance=self,
        )

    def _consume_resources(self):
        resource_recipe = self.action_template.consumed_resources()
        patient_inventory = self.patient_instance.inventory
        area_inventory = self.patient_instance.area.inventory
        for resource, amount in resource_recipe.items():
            pulled_resources = patient_inventory.resource_stock(resource) - amount
            if pulled_resources < 0:
                area_inventory.transition_resource_to(
                    patient_inventory, resource, -pulled_resources
                )
            if not resource.is_returnable:
                patient_inventory.change_resource(resource, -amount)

    def _application_finished_strategy(self):
        self.patient_instance.remove_from_queue(self)

        if self.action_template.effect_duration != None:
            ScheduledEvent.create_event(
                self.patient_instance.exercise,
                self.action_template.effect_duration,  # ToDo: Replace with scalable local time system
                "_effect_expired",
                patient_action_instance=self,
            )
            self._update_state(ActionInstanceStateNames.IN_EFFECT)

    def _effect_expired(self):
        self._update_state(ActionInstanceStateNames.EXPIRED)


def get_action_instance_class_from_string(action_instance_str):
    if action_instance_str == "patient_action_instance":
        return PatientActionInstance
    elif action_instance_str == "lab_action_instance":
        return LabActionInstance
    else:
        raise ValueError("ActionInstance type not recognized")


class LabActionInstance(ActionInstance):
    constraints = [one_or_more_field_not_null(["area", "lab"], "lab_action_instance")]
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        LabActionInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    @classmethod
    def create(cls, action_template, lab, area=None, patient_instance=None):
        obj = super().create(
            action_template,
            place_of_application=lab,
            lab=lab,
            area=area,
            patient_instance=patient_instance,
        )
        return obj

    def _check_application_status(self):
        raise NotImplementedError("Should be available after condition checking")
        # return self.action_template.application_status(self.lab, self.area)

    def _create_scheduled_event(self, duration, scheduled_method):
        return ScheduledEvent.create_event(
            self.lab.exercise,
            duration,  # ToDo: Replace with scalable local time system
            scheduled_method,
            lab_action_instance=self,
        )

    def _consume_resources(self):
        resource_recipe = self.action_template.consumed_resources()
        inventory = self.lab.inventory
        for resource, amount in resource_recipe.items():
            inventory.change_resource(resource, -amount)

    def _application_finished_strategy(self):
        self.lab.remove_from_queue(self)
        self._return_applicable_resources()
        if self.action_template.produced_resources():
            self._produce_resources(self.action_template.produced_resources())

    def _return_applicable_resources(self):
        inventory = self.lab.inventory
        resource_recipe = self.action_template.consumed_resources()

        for resource, amount in resource_recipe.items():
            if resource.is_returnable:
                inventory.change_resource(resource, amount)

    def _produce_resources(self, resource_recipe):
        if not resource_recipe:
            raise Exception(
                "Resource production was called without resources to produce"
            )
        for resource, amount in resource_recipe.items():
            self.area.inventory.change_resource(resource, amount)
