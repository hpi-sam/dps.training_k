from django.db import models
from game.models import ScheduledEvent
from template.models import Action
from game.channel_notifications import ActionInstanceDispatcher
from helpers.local_timable import LocalTimeable


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
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, blank=True, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, blank=True, null=True)
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
        ActionInstanceDispatcher.save_and_notify(self, changes, *args, **kwargs)

    def _update_state(self, state_name, info_text=None):
        new_state = self.current_state.update(
            state_name, self.get_local_time(), info_text
        )
        if new_state:
            self.current_state = new_state
            self.save(update_fields=["current_state"])
        return self.current_state

    @classmethod
    def create(cls, action_template, patient_instance=None, area=None):
        if not patient_instance and not area:
            raise ValueError(
                "Either patient_instance or area must be provided - an action instance always need a context"
            )

        is_applicable, context = action_template.application_status(
            patient_instance, patient_instance.area
        )
        action_instance = ActionInstance.objects.create(
            patient_instance=patient_instance,
            area=area,
            action_template=action_template,
        )
        if is_applicable:
            action_instance.current_state = ActionInstanceState.objects.create(
                action_instance=action_instance,
                name=ActionInstanceStateNames.PLANNED,
                t_local_begin=action_instance.get_local_time(),
            )
            action_instance.save(update_fields=["current_state"])
            action_instance.place_of_application().register_to_queue(action_instance)
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
        self._return_applicable_resources()
        self.place_of_application().remove_from_queue(self)

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

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def place_of_application(self):
        if self.action_template.category == Action.Category.LAB:
            return self.patient_instance.area
        return self.patient_instance

    def _consume_resources(self):
        inventory = self.place_of_application().consuming_inventory
        resource_recipe = self.action_template.get_resources()
        for resource, amount in resource_recipe.items():
            inventory.change_resource(resource, -amount)

    def _return_applicable_resources(self):
        inventory = self.place_of_application().consuming_inventory
        resource_recipe = self.action_template.get_resources()

        for resource, amount in resource_recipe.items():
            if resource.is_returnable:
                inventory.change_resource(resource, amount)
