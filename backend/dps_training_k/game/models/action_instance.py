from django.db import models
from game.models import ScheduledEvent, Patient, Area
from template.models import Action
from game.channel_notifications import ActionInstanceDispatcher
from helpers.local_timable import LocalTimeable


class ActionInstanceStateNames(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    ON_HOLD = "OH", "on_hold"
    FINISHED = "FI", "finished"
    ACTIVE = "AC", "active"

    DECLINED = "DE", "declined"
    CANCELED = "CA", "canceled"


class ActionInstanceState(models.Model):
    action_instance = models.ForeignKey(
        "ActionInstance",
        on_delete=models.CASCADE,
        related_name="timestamps",
    )
    name = models.CharField(choices=ActionInstanceStateNames.choices, max_length=2)
    t_local_begin = models.IntegerField()
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )
    info_text = models.CharField(null=True, blank=True, default=None)

    def update(self, state, time):
        if state == self.state_name:
            return False, None
        self.t_local_end = time
        self.save(update_fields=["t_local_end"])
        return True, ActionInstanceState.objects.create(
            action_instance=self.action_instance, state=state, time=time
        )


class ActionInstance(LocalTimeable, models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    current_state = models.ForeignKey(
        "ActionInstanceState", on_delete=models.CASCADE, blank=True, null=True
    )
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )

    @property
    def name(self):
        return self.action_template.name

    @property
    def state_name(self):
        return self.state.name

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ActionInstanceDispatcher.save_and_notify(self, changes, *args, **kwargs)

    def _update_state(self, state_name):
        state_changed, new_state = self.current_timestamp.update(
            self, state_name, self.get_local_time()
        )
        if state_changed:
            self.current_state = new_state
            super().save(update_fields=["current_state"])

    @classmethod
    def create(cls, patient, action_template):
        is_applicable, context = action_template.application_status(
            patient, patient.area
        )
        action_instance = ActionInstance(
            patient=patient,
            action_template=action_template,
        )
        if is_applicable:
            action_instance.state = ActionInstanceState.objects.create(
                action_instance=action_instance,
                name=ActionInstanceStateNames.PLANNED,
                t_local_begin=action_instance.get_local_time(),
            )
            action_instance.save()
            state=ActionInstanceState.PLANNED,
            return action_instance
        action_instance.current_timestamp = ActionInstanceState.objects.create(
            action_instance=action_instance,
            name=ActionInstanceStateNames.DECLINED,
            t_local_begin=action_instance.get_local_time(),
        )
        action_instance.state.info_text = context
        action_instance.save()
        return action_instance

    def try_application(self):
        is_applicable, context = self.action_template.application_status(
            self.patient, self.patient.area
        )
        if not is_applicable:
            action_instance.state = ActionInstanceState.DECLINED
            action_instance.current_timestamp.state_name = ActionInstanceState.DECLINED
            action_instance.reason_of_declination = context
            action_instance.save()
            return False
        action_instance.save()
        return action_instance.try_application()

    def place_of_application(self):
        if self.action_template.category == Action.Category.LAB:
            return Area
        return Patient

    def start_application(self):
        ScheduledEvent.create_event(
            self.patient.exercise,
            self.action_template.duration,  # ToDo: Replace with scalable local time system
            "application_finished",
            applied_action=self,
        )
        self.state = ActionInstanceState.IN_PROGRESS
        self.save(update_fields=["state"])

    def application_finished(self):
        self.state = ActionInstanceState.FINISHED
        self.save(update_fields=["state"])

    def _update_timestamp(self):
        timestamp_changed, new_timestamp = self.current_timestamp.update(
            self, self.state, self.get_local_time()
        )
        if timestamp_changed:
            self.current_timestamp = new_timestamp
            super().save(update_fields=["current_timestamp"])
