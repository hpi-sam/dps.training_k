from django.db import models

from game.channel_notifications import ActionInstanceDispatcher
from game.models import ScheduledEvent, MaterialInstance
from helpers.fields_not_null import one_or_more_field_not_null
from helpers.local_timable import LocalTimeable


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

    @property
    def is_cancelable(self):
        return self.name in [
            ActionInstanceStateNames.PLANNED,
            ActionInstanceStateNames.IN_PROGRESS,
            ActionInstanceStateNames.ON_HOLD,
        ]

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

    destination_area = models.ForeignKey(
        "Area", on_delete=models.CASCADE, blank=True, null=True, related_name="+"
    )  # querying Area.objects.actioninstance_set is not supported atm as area field is also set for production/shifting actions
    template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    current_state = models.ForeignKey(
        "ActionInstanceState", on_delete=models.CASCADE, blank=True, null=True
    )
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.IntegerField(null=True)
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, blank=True, null=True
    )
    historic_patient_state = models.ForeignKey(
        "template.PatientState", on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def completed(self):
        if self.current_state in ActionInstanceState.completion_states():
            return True
        else:
            return False

    @property
    def exercise(self):
        if self.patient_instance:
            return self.patient_instance.exercise
        if self.lab:
            return self.lab.exercise

    @property
    def name(self):
        return self.template.name

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
    def state_name(self):
        if self.current_state != None:
            return self.current_state.name
        else:
            return None

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ActionInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def delete(self, using=None, keep_parents=False):
        ActionInstanceDispatcher.delete_and_notify(self)

    def _update_state(self, state_name, info_text=None):
        new_state = self.current_state.update(
            state_name, self.get_local_time(), info_text
        )
        if new_state:
            self.current_state = new_state
            self.save(update_fields=["current_state"])
        return self.current_state

    @classmethod
    def create(cls, template, patient_instance=None, destination_area=None, lab=None):
        if not patient_instance and not lab:
            raise ValueError(
                "Either patient_instance or lab must be provided - an action instance always need a message"
            )
        if not destination_area and template.relocates:
            destination_area = patient_instance.area
        action_instance = ActionInstance.objects.create(
            patient_instance=patient_instance,
            destination_area=destination_area,
            lab=lab,
            template=template,
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
        if not self.attached_instance().can_receive_actions():
            is_applicable, message = (
                False,
                f"{self.attached_instance().frontend_model_name()} kann keine Aktionen mehr empfangen",
            )
        elif self.patient_instance and self.patient_instance.is_absent():
            is_applicable, message = (
                False,
                f"{self.patient_instance.name} ist bereits woanders",
            )
        else:
            resources_to_block, message, is_applicable = self._try_acquiring_resources(
                self.attached_instance(), self.attached_instance()
            )
            if is_applicable:
                is_applicable, relocates, message = self._check_relocating()

        if not is_applicable:
            self._update_state(ActionInstanceStateNames.ON_HOLD, message)
            return False, message

        for resource in resources_to_block:
            resource.block(self)
        if relocates:
            self._try_relocating()
        self._start_application()
        return True, None

    def _start_application(self):
        if not self.patient_instance and not self.lab:
            raise ValueError(
                "An action instance always needs a patient instance or lab to be scheduled"
            )
        exercise = (
            self.patient_instance.exercise
            if self.patient_instance
            else self.lab.exercise
        )
        ScheduledEvent.create_event(
            exercise,
            self.template.application_duration,  # ToDo: Replace with scalable local time system
            "_application_finished",
            action_instance=self,
        )

        if self.template.category == self.template.Category.EXAMINATION:
            self.historic_patient_state = self.patient_instance.patient_state
            self.save(update_fields=["historic_patient_state"])
        self._update_state(ActionInstanceStateNames.IN_PROGRESS)
        self._consume_resources()

    def _application_finished(self):
        self._update_state(
            ActionInstanceStateNames.FINISHED,
            info_text=self.template.get_result(self),
        )
        self._free_resources()
        self._try_resource_production()
        self._try_returning()
        self._try_starting_action_effects()

    def try_cancelation(self) -> tuple[bool, str]:
        """Returns whether the object was canceled successfully and an error message if not."""

        if not self.current_state.is_cancelable:
            return (
                False,
                f"Aktionen mit dem Status {self.current_state.get_name_display()} können nicht abgebrochen werden.",
            )

        if self.template.relocates:
            return False, f"Aktion {self.template.name} kann nicht abgebrochen werden."

        self.owned_events.all().delete()
        self._free_resources()

        self._update_state(
            ActionInstanceStateNames.CANCELED, "Aktion wurde abgebrochen."
        )

        return True, ""

    def attached_instance(self):
        if self.template.location == self.template.Location.BEDSIDE:
            return self.patient_instance
        if self.template.location == self.template.Location.LAB:
            return self.lab
        else:
            raise ValueError("No attached instance found")

    def _check_relocating(self):
        """
        :return bool, bool, str: True if the action is applicable, True if the action relocates. If the action doesn't relocate,
        the string contains the reason for declination
        """
        if not self.template.relocates:
            return True, False, ""
        is_applicable, message = self.patient_instance.check_moving_to(self.lab)
        return is_applicable, is_applicable, message

    def _try_relocating(self):
        """
        iff the action is an action that relocates, the patient is moved to the lab
        :return bool, str: True if the moving is legal, either by not requiring movements or by succeeding a required movement.
        If False, the str contains the reason why the action is not applicable.
        """
        is_applicable, relocates, message = self._check_relocating()
        if not is_applicable or not relocates:
            return is_applicable, message
        self.destination_area = self.patient_instance.area
        self.save(update_fields=["destination_area"])
        self.patient_instance.try_moving_to(self.lab)
        return True, message

    def _try_returning(self):
        """
        iff the action is an action that relocated, the patient is moved back to the destination area
        """
        if self.template.relocates:
            self.patient_instance._perform_move(self.destination_area)
            return True
        return False

    def _try_resource_production(self):
        if self.template.category == self.template.Category.PRODUCTION:
            MaterialInstance.generate_materials(
                self.template.produced_resources(), self.destination_area
            )
            return True
        return False

    def _try_starting_action_effects(self):
        if self.template.effect_duration != None:
            ScheduledEvent.create_event(
                self.patient_instance.exercise,
                self.template.effect_duration,  # ToDo: Replace with scalable local time system
                "_effect_expired",
                action_instance=self,
            )
            self._update_state(ActionInstanceStateNames.IN_EFFECT)
            return True
        return False

    def _effect_expired(self):
        self._update_state(ActionInstanceStateNames.EXPIRED)

    def __str__(self):
        return f"""ActionInstance {self.template.name} for 
            {self.patient_instance.name + str(self.patient_instance.id) 
             if self.patient_instance 
             else "Lab " + str(self.lab.exercise.frontend_id)}"""

    def _try_acquiring_resources(self, material_owner, personnel_owner):
        """
        :params material_owner: Instance having a material_available method
        :params personell_owner: Instance having a personell_available method
        :return list, str, bool: True if all resources might be aquired for satisfying the starting condition, False if not.
        If true, the list returns all resources needed to satisfy the condition. If false, the str contains the reason for failing
        """
        needed_material_groups = self.template.material_needed()
        if not needed_material_groups:
            needed_material_groups = []
        resources_to_block = []
        for needed_material_group in needed_material_groups:
            resource_found = False

            for material_condition in needed_material_group:
                available_materials = material_owner.material_available(
                    material_condition
                )
                if available_materials:
                    resources_to_block.append(available_materials[0])
                    resource_found = True
                    break
            if not resource_found:
                return (
                    [],
                    f"Kein Material des Typs {material_condition.name} verfügbar",
                    False,
                )

        available_personnel = personnel_owner.personnel_available()
        if len(available_personnel) < self.template.personnel_count_needed():
            return [], False, f"Nicht genug Personal verfügbar"
        for i in range(self.template.personnel_count_needed()):
            resources_to_block.append(available_personnel[i])
        if not resources_to_block:
            return [], "", True
        return resources_to_block, "", True

    def _free_resources(self):
        for material in self.materialinstance_set.all():
            if material.is_reusable:
                material.release()
        for personnel in self.personnel_set.all():
            personnel.release()

    def _consume_resources(self):
        for material in self.materialinstance_set.all():
            if not material.is_reusable:
                material.consume()

    def get_patient_examination_codes(self) -> dict[str, str]:
        codes = {}
        if self.historic_patient_state:
            codes.update(
                {
                    str(k): str(v)
                    for k, v in self.historic_patient_state.examination_codes.items()
                }
            )
        if self.patient_instance and self.patient_instance.static_information:
            codes.update(
                {
                    str(k): str(v)
                    for k, v in self.patient_instance.static_information.examination_codes.items()
                }
            )
        return codes
