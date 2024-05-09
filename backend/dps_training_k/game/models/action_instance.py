from collections import Counter
from django.db import models

from game.channel_notifications import ActionInstanceDispatcher
from game.models import ScheduledEvent, MaterialInstance
from helpers.local_timable import LocalTimeable
from helpers.one_or_more_field_not_null import one_or_more_field_not_null


class ActionInstanceStateNames(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    ON_HOLD = "OH", "on_hold"
    FINISHED = "FI", "finished"
    IN_EFFECT = "IE", "in effect"
    EXPIRED = "EX", "expired"
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
        return [ActionInstanceStateNames.FINISHED, ActionInstanceStateNames.IN_EFFECT]

    def completion_states():
        return [ActionInstanceStateNames.FINISHED, ActionInstanceStateNames.EXPIRED]


class ActionInstance(LocalTimeable, models.Model):
    class Meta:
        ordering = ["order_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["order_id", "patient_instance"],
                name="unique_order_id_for_patient",
            ),
            one_or_more_field_not_null(["patient_instance", "lab"], "action"),
        ]

    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, blank=True, null=True
    )
    area = models.ForeignKey(
        "Area", on_delete=models.CASCADE, blank=True, null=True, related_name="+"
    )  # querying Area.objects.actioninstance_set is not supported atm as area field is also set for production/shifting actions
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, blank=True, null=True)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    current_state = models.ForeignKey(
        "ActionInstanceState", on_delete=models.CASCADE, blank=True, null=True
    )
    order_id = models.IntegerField(null=True)

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
    def create(cls, action_template, patient_instance=None, area=None, lab=None):
        if not patient_instance and not area:
            raise ValueError(
                "Either patient_instance or lab must be provided - an action instance always need a context"
            )

        action_instance = ActionInstance.objects.create(
            patient_instance=patient_instance,
            area=area,
            lab=lab,
            action_template=action_template,
            order_id=ActionInstance.generate_order_id(patient_instance),
        )
        action_instance.current_state = ActionInstanceState.objects.create(
            action_instance=action_instance,
            name=ActionInstanceStateNames.PLANNED,
            t_local_begin=action_instance.get_local_time(),
        )
        action_instance.save(update_fields=["current_state"])
        return action_instance

    @classmethod
    def generate_order_id(self, patient_instance):
        # Use aggregate to find the maximum order_id for the specified patient_instance
        result = ActionInstance.objects.filter(
            patient_instance=patient_instance
        ).aggregate(max_order_id=models.Max("order_id"))
        max_order_id = result["max_order_id"]
        if max_order_id is None:
            new_order_id = 0
        else:
            new_order_id = max_order_id + 1
        return new_order_id

    def try_application(self):
        if self.patient_instance:
            is_applicable, context = self.action_template.application_status(
                self._available_materials_count(),
                patient_instance=self.patient_instance,
                area=self.patient_instance.area,
            )
        elif self.lab:
            is_applicable, context = self.action_template.application_status(
                self._available_materials_count(),
                lab=self.lab,
                area=self.area,
            )
        if not is_applicable:
            self._update_state(ActionInstanceStateNames.ON_HOLD, context)
            return False
        self._start_application()
        return True

    def _start_application(self):
        if not self.patient_instance and not self.lab:
            raise ValueError(
                "An action instance always needs a patient instance or lab to be scheduled"
            )
        if self.patient_instance:
            ScheduledEvent.create_event(
                self.patient_instance.exercise,
                self.action_template.application_duration,  # ToDo: Replace with scalable local time system
                "_patient_application_finished",
                action_instance=self,
                patient_state=self.patient_instance.patient_state.data,
            )
        if self.lab:
            ScheduledEvent.create_event(
                self.lab.exercise,
                self.action_template.application_duration,  # ToDo: Replace with scalable local time system
                "_lab_application_finished",
                action_instance=self,
            )

        self._update_state(ActionInstanceStateNames.IN_PROGRESS)

    def _patient_application_finished(self, patient_state):
        self._update_state(
            ActionInstanceStateNames.FINISHED,
            info_text=self.action_template.get_result(patient_state),
        )
        self._application_finished()

    def _lab_application_finished(self):
        self._update_state(
            ActionInstanceStateNames.FINISHED,
            info_text=self.action_template.get_result(),
        )
        self._application_finished()

    def _application_finished(self):
        if self.action_template.produced_resources() != None:
            MaterialInstance.generate_materials(
                self.action_template.produced_resources(), self.area
            )
        if self.action_template.effect_duration != None:
            ScheduledEvent.create_event(
                self.patient_instance.exercise,
                self.action_template.effect_duration,  # ToDo: Replace with scalable local time system
                "_effect_expired",
                action_instance=self,
            )
            self._update_state(ActionInstanceStateNames.IN_EFFECT)

    def _effect_expired(self):
        self._update_state(ActionInstanceStateNames.EXPIRED)

    def _available_materials_count(self):
        material_types = [
            material_instance.material_template
            for material_instance in self._available_materials()
        ]
        material_type_occurences = dict(Counter(material_types))
        return material_type_occurences

    def _available_materials(self):
        if self.patient_instance:
            return self.patient_instance.materialinstance_set.filter(is_blocked=False)
        return self.lab.materialinstance_set.filter(is_blocked=False)
