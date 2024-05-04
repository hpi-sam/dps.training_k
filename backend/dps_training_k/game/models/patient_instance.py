from django.db import models

from game.channel_notifications import PatientInstanceDispatcher
from helpers.actions_queueable import ActionsQueueable
from helpers.eventable import Eventable
from helpers.triage import Triage
from template.models.patient_state import PatientState
from .scheduled_event import ScheduledEvent

from .inventory import Inventory


class PatientInstance(Eventable, ActionsQueueable, models.Model):

    name = models.CharField(max_length=100, default="Max Mustermann")
    static_information = models.ForeignKey(
        "template.PatientInformation",
        on_delete=models.CASCADE,
        null=True,  # for migration purposes
    )  # via Sensen ID
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    area = models.ForeignKey(
        "Area",
        on_delete=models.CASCADE,
        null=True,  # for debugging purposes
        blank=True,  # for debugging purposes
    )
    inventory = models.OneToOneField("Inventory", on_delete=models.CASCADE)
    patient_state = models.ForeignKey(
        PatientState,
        on_delete=models.SET_NULL,
        null=True,  # for debugging purposes
        default=None,  # for debugging purposes
    )
    patient_frontend_id = models.IntegerField(
        unique=True,
        help_text="patient_frontend_id used to log into patient - therefore part of authentication",
    )
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.inventory = Inventory.objects.create()
        changes = kwargs.get("update_fields", None)
        PatientInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def delete(self, using=None, keep_parents=False):
        PatientInstanceDispatcher.delete_and_notify(self)

    def schedule_state_change(self):
        from game.models import ScheduledEvent

        if self.patient_state.is_dead:
            return False
        if self.patient_state.is_final():
            return False
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "execute_state_change",
            patient=self,
        )

    def execute_state_change(self):
        if self.patient_state.is_dead or self.patient_state.is_final():
            raise Exception(
                "Patient is dead or in final state, state change should have never been scheduled"
            )
        state_change_requirements = {"self.condition_checker.now()": ""}
        future_state = self.patient_state.transition.activate(state_change_requirements)
        if not future_state:
            return False
        self.patient_state = future_state
        self.save(update_fields=["patient_state"])
        self.schedule_state_change()
        return True

    def start_action(self, action_template):
        from game.models import PatientActionInstance

        action_instance = PatientActionInstance.create(
            action_template=action_template,
            patient_instance=self,
        )
        action_instance.try_application()
        return action_instance

    def take_resource(self, resource, amount):
        area_inventory = self.area.inventory
        if area_inventory.resource_stock(resource) < amount:
            raise ValueError(
                f"Area does not have enough resources {resource.name} to take"
            )
        area_inventory.transition_resource_to(self.inventory, resource, amount)

    def return_resource(self, resource, amount):
        if self.inventory.resource_stock(resource) < amount:
            raise ValueError(
                f"Patient does not have enough resources {resource.name} to return"
            )
        area_inventory = self.area.inventory
        self.inventory.transition_resource_to(area_inventory, resource, amount)

    def is_dead(self):
        if self.patient_state.is_dead:
            return True
        return False

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with ID {self.patient_id}"
