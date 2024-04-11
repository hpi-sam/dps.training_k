from django.db import models
from game.models import ScheduledEvent, Patient, Area
from template.models import Action
from game.channel_notifications import ActionInstanceDispatcher


class ActionInstanceState(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    FINISHED = "FI", "finished"
    ACTIVE = "AC", "active"

    DECLINED = "DE", "declined"
    CANCELED = "CA", "canceled"


class ActionInstanceTimestamp(models.Model):
    action_instance = models.OneToOneField(
        "ActionInstance",
        on_delete=models.CASCADE,
        related_name="timestamps",
    )
    state_name = models.CharField(choices=ActionInstanceState.choices, max_length=2)
    t_local_begin = models.IntegerField()
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )

    def update(self, state, time):
        if state == self.state_name:
            return False, None
        self.t_local_end = time
        self.save(update_fields=["t_local_end"])
        return True, ActionInstanceTimestamp.objects.create(
            action_instance=self.action_instance, state=state, time=time
        )


class ActionInstance(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    state = models.CharField(
        choices=ActionInstanceState.choices,
        default=ActionInstanceState.PLANNED,
        max_length=2,
    )
    current_timestamp = models.ForeignKey(
        "ActionInstanceTimestamp", on_delete=models.CASCADE, blank=True, null=True
    )
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )

    @property
    def name(self):
        return self.action_template.name

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ActionInstanceDispatcher.save_and_notify(self, changes, *args, **kwargs)
        self._update_timestamp()

    def try_application(self):
        is_applicable, context = self.action_template.application_status(
            self.patient, self.patient.area
        )
        if not is_applicable:
            self.state = ActionInstanceState.DECLINED
            self.reason_of_declination = context
            self.save(update_fields=["state", "reason_of_declination"])
            return False

        is_next = self.place_of_application().is_next_action(self)
        if is_next:
            self.start_application()
            return True

    @classmethod
    def create(cls, patient, action_template):
        is_applicable, context = action_template.application_status(
            patient, patient.area
        )
        action_instance = ActionInstance(
            patient=patient,
            action_template=action_template,
            state=ActionInstanceState.PLANNED,
        )
        action_instance.current_timestamp = ActionInstanceTimestamp.objects.create(
            action_instance=action_instance,
            state_name=ActionInstanceState.PLANNED,
            t_local_begin=action_instance.get_local_time(),
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
