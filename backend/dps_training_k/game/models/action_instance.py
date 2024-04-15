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
        related_name="states",
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
        if state == ActionInstanceStateNames.DECLINED:
            raise ValueError("Once Declined, states cannot be changed")
        self.t_local_end = time
        self.save(update_fields=["t_local_end"])
        return True, ActionInstanceState.objects.create(
            action_instance=self.action_instance, state=state, time=time
        )


class ActionInstance(LocalTimeable, models.Model):
    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, blank=True, null=True
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

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ActionInstanceDispatcher.save_and_notify(self, changes, *args, **kwargs)

    def _update_state(self, state_name):
        state_changed, new_state = self.current_state.update(
            self, state_name, self.get_local_time()
        )
        if state_changed:
            self.current_state = new_state
            super().save(update_fields=["current_state"])

    @classmethod
    def create(cls, action_template, patient=None, area=None):
        is_applicable, context = action_template.application_status(
            patient, patient.area
        )
        action_instance = ActionInstance(
            patient=patient,
            area=area,
            action_template=action_template,
        )
        if is_applicable:
            action_instance.state = ActionInstanceState.objects.create(
                action_instance=action_instance,
                name=ActionInstanceStateNames.PLANNED,
                t_local_begin=action_instance.get_local_time(),
            )
            action_instance.save()
            action_instance.place_of_application().register_to_queue(action_instance)
            return action_instance
        action_instance.state = ActionInstanceState.objects.create(
            action_instance=action_instance,
            name=ActionInstanceStateNames.DECLINED,
            t_local_begin=action_instance.get_local_time(),
        )
        action_instance.state.info_text = context
        action_instance.state.save()
        action_instance.save()
        return action_instance

    def try_application(self):
        if self.state_name == ActionInstanceStateNames.DECLINED:
            raise ValueError("Cannot start a declined action")

        is_applicable, context = self.action_template.application_status(
            self.patient, self.patient.area
        )
        if not is_applicable:
            entered_on_hold, new_state = self._update_state(
                ActionInstanceStateNames.ON_HOLD
            )
            if entered_on_hold:
                self.state = new_state
                self.save(update_fields=["state"])
            self.state.info_text = self.state.info_text + context
            self.state.save(update_fields=["info_text"])
            return False

        self._start_application()
        return True

    def place_of_application(self):
        if self.action_template.category == Action.Category.LAB:
            return self.patient.area
        return self.patient

    def _start_application(self):
        ScheduledEvent.create_event(
            self.patient.exercise,
            self.action_template.application_duration,  # ToDo: Replace with scalable local time system
            "application_finished",
            applied_action=self,
        )
        self.state = ActionInstanceStateNames.IN_PROGRESS
        self.save(update_fields=["state"])

    def _application_finished(self):
        self.state = ActionInstanceStateNames.FINISHED
        self.save(update_fields=["state"])
