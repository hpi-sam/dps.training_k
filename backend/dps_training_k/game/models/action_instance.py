from abc import abstractmethod
from django.db import models
from game.models import ScheduledEvent
from template.models import Action
from game.channel_notifications import ActionInstanceDispatcher
from helpers.local_timable import LocalTimeable
from helpers.one_field_not_null import one_or_more_field_not_null


class ActionInstanceStateNames(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    ON_HOLD = "OH", "on_hold"
    FINISHED = "FI", "finished"
    ACTIVE = "AC", "active"
    EXPIRED = "EX", "expired"

    DECLINED = "DE", "declined"
    CANCELED = "CA", "canceled"


class ActionInstanceState(models.Model):
    """
    State switching & information logic for ActionInstance
    """

    action_instance = models.ForeignKey(
        "ActionInstance",
        on_delete=models.CASCADE,
        related_name="states",
    )
    name = models.CharField(choices=ActionInstanceStateNames.choices, max_length=2)
    t_local_begin = models.IntegerField()
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )
    info_text = models.CharField(null=True, blank=True, default=None)

    def update(self, state_name, time, info_text=None):
        if self.name == ActionInstanceStateNames.DECLINED:
            raise ValueError("Once Declined, states cannot be changed")
        if state_name == self.name and not info_text:
            return None
        if state_name == self.name and info_text:
            self.add_info(info_text)
            return None
        self.t_local_end = time
        self.save(update_fields=["t_local_end"])
        return ActionInstanceState.objects.create(
            action_instance=self.action_instance,
            name=state_name,
            t_local_begin=time,
            info_text=info_text,
        )

    def add_info(self, info_text):
        self.info_text = self.info_text + info_text
        self.save(update_fields=["info_text"])

    def success_states():
        return [ActionInstanceStateNames.FINISHED, ActionInstanceStateNames.ACTIVE]


class ActionInstance(LocalTimeable, models.Model):
    """
    Behaviour Strategy for ActionInstances. Should be expanded by subclasses. Triggers State changes.
    """

    class Meta:
        constraints = [
            one_or_more_field_not_null(
                ["patient_instance", "area", "lab"], "action_instance"
            )
        ]

    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, blank=True, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, blank=True, null=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, blank=True, null=True)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    current_state = models.ForeignKey(
        "ActionInstanceState", on_delete=models.CASCADE, blank=True, null=True
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

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ActionInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

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
                "Either patient_instance or area must be provided - an action instance always need a context"
            )

        is_applicable, context = action_template.application_status(
            patient_instance, patient_instance.area
        )
        action_instance = ActionInstance.objects.create(
            action_template=action_template,
            patient_instance=patient_instance,
            area=area,
            lab=lab,
        )
        if is_applicable:
            action_instance.current_state = ActionInstanceState.objects.create(
                action_instance=action_instance,
                name=ActionInstanceStateNames.PLANNED,
                t_local_begin=action_instance.get_local_time(),
            )
            action_instance.save(update_fields=["current_state"])
            place_of_application.register_to_queue(action_instance)
            return action_instance
        action_instance.current_state = ActionInstanceState.objects.create(
            action_instance=action_instance,
            name=ActionInstanceStateNames.DECLINED,
            t_local_begin=action_instance.get_local_time(),
            info_text=context,
        )
        action_instance.save(update_fields=["current_state"])
        return action_instance

    def try_application(self):
        if self.state_name == ActionInstanceStateNames.DECLINED:
            raise ValueError("Cannot start a declined action")

        is_applicable, context = self.action_template.application_status(
            self.patient_instance, self.patient_instance.area
        )
        if not is_applicable:
            self._update_state(ActionInstanceStateNames.ON_HOLD, context)
            return False

        self._start_application()
        return True

    def _start_application(self):
        ScheduledEvent.create_event(
            self.patient_instance.exercise,
            self.action_template.application_duration,  # ToDo: Replace with scalable local time system
            "_application_finished",
            action_instance=self,
        )
        self._consume_resources()
        self._update_state(ActionInstanceStateNames.IN_PROGRESS)

    def _application_finished(self):
        self._update_state(
            ActionInstanceStateNames.FINISHED,
            info_text=self.action_template.get_result(
                self.patient_instance.patient_state
            ),
        )
        self._application_finished_strategy()

    @abstractmethod
    def _consume_resources(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _application_finished_strategy(self):
        raise NotImplementedError("Subclasses must implement this method")


class LabActionInstance(ActionInstance):
    class Meta:
        proxy = True

    @classmethod
    def create(cls, action_template, lab, area=None, patient_instance=None):
        return super().create(
            action_template,
            place_of_application=lab,
            lab=lab,
            area=area,
            patient_instance=patient_instance,
        )

    def _consume_resources(self):
        resource_recipe = self.action_template.consumed_resources()
        inventory = self.lab.consuming_inventory
        for resource, amount in resource_recipe.items():
            inventory.change_resource(resource, -amount)

    def _application_finished_strategy(self):
        self.lab.remove_from_queue(self)
        self._return_applicable_resources()
        if self.action_template.produced_resources():
            self._produce_resources()

    def _return_applicable_resources(self):
        inventory = self.lab.consuming_inventory
        resource_recipe = self.action_template.consumed_resources()

        for resource, amount in resource_recipe.items():
            if resource.is_returnable:
                inventory.change_resource(resource, amount)

    def _produce_resources(self, resource_recipe):
        if not resource_recipe:
            raise Exception(
                "Resource production was called without resources to produce"
            )
        inventory = self.lab.consuming_inventory
        for resource, amount in resource_recipe.items():
            inventory.change_resource(resource, amount)


class PatientActionInstance(ActionInstance):
    class Meta:
        proxy = True

    @classmethod
    def create(cls, action_template, patient_instance, area):
        return super().create(
            action_template,
            place_of_application=patient_instance,
            area=area,
            patient_instance=patient_instance,
        )

    def _consume_resources(self):
        resource_recipe = self.action_template.consumed_resources()
        patient_inventory = self.patient_instance.consuming_inventory
        area_inventory = self.patient_instance.area.consuming_inventory
        for resource, amount in resource_recipe.items():
            pulled_resources = patient_inventory.resource_stock(resource) - amount
            if pulled_resources < 0:
                area_inventory.transition_resource_to(
                    patient_inventory, resource, pulled_resources
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
                action_instance=self,
            )
            self._update_state(ActionInstanceStateNames.ACTIVE)

    def _effect_expired(self):
        self._update_state(ActionInstanceStateNames.EXPIRED)
