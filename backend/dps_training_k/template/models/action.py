import logging
import uuid

from django.db import models

from helpers.models import UUIDable
from .material import Material


class Action(UUIDable, models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        PRODUCTION = "PR", "production"
        OTHER = "OT", "other"

    class Location(models.TextChoices):
        LAB = "LA", "lab"
        BEDSIDE = "BE", "bedside"
        STATION = "ST", "station"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=Category.choices, max_length=2)
    location = models.CharField(
        choices=Location.choices, max_length=2, default=Location.BEDSIDE
    )
    relocates = models.BooleanField(
        default=False,
        help_text="Does the action relocate the patient to the location and back?",
    )
    application_duration = models.IntegerField(
        default=10,
        help_text="Duration in seconds in realtime. Might be scaled by external factors.",
    )
    effect_duration = models.IntegerField(
        default=None,
        null=True,
        help_text="Effect duration in seconds in realtime. Might be scaled by external factors.",
    )
    conditions = models.JSONField(null=True, blank=True, default=None)
    results = models.JSONField(null=True, blank=True, default=None)

    def produced_resources(self):
        if not self.results:
            return None
        if not "produced_material" in self.results:
            return None
        resources = self.results["produced_material"]
        resources = {
            Material.objects.get(uuid=uuid.UUID(key)): amount
            for key, amount in resources.items()
        }
        return resources

    def material_needed(self):
        """
        :return list of lists: each list entry means that at least
        one of the materials in the list is needed to perfom this action
        """
        if not self.conditions:
            return []
        if not "material" in self.conditions:
            return []
        material_uuids = self.conditions["material"] or []
        # currently, lab_devices and material do exactly the same thing, hence they can be handled the same. If that changes, the following two lines are a bad idea
        lab_device_uuids = self.conditions["lab_devices"] or []
        material_uuids += lab_device_uuids
        if not material_uuids:
            return []

        needed_material_groups = []
        for material_condition_uuid in material_uuids:
            if isinstance(material_condition_uuid, list):
                needed_material_group = [
                    Material.objects.get(uuid=uuid.UUID(material_uuid))
                    for material_uuid in material_condition_uuid
                ]
                needed_material_groups.append(needed_material_group)
        needed_single_material = [
            [Material.objects.get(uuid=uuid.UUID(material_uuid))]
            for material_uuid in material_uuids
            if not isinstance(material_uuid, list)
        ]
        return needed_material_groups + needed_single_material

    def personnel_count_needed(self):
        if self.location == Action.Location.LAB:
            return 0  # ToDo: remove once we use personnel for labs
        if not self.conditions:
            return 0
        if not "num_personnel" in self.conditions:
            return 0
        return (
            self.conditions["num_personnel"] if self.conditions["num_personnel"] else 0
        )
    
    def required_actions(self):
        return self.get_action_conditions("required_actions")

    def prohibitive_actions(self):
        return self.get_action_conditions("prohibitive_actions")

    def get_action_conditions(self, conditions_type):
        """
        :return list of lists: each list entry means that at least
        one of the actions in the list is needed to fulfill the corresponding condition
        """
        if not self.conditions:
            return []
        if not conditions_type in self.conditions:
            return []
        action_conditions = self.conditions[conditions_type] or []

        action_groups = []
        single_actions = []
        for action_condition in action_conditions:
            if isinstance(action_condition, list):
                action_group = [
                    Action.objects.get(uuid=uuid.UUID(action_uuid))
                    for action_uuid in action_condition
                ]
                action_groups.append(action_group)
            else:
                single_actions.append([Action.objects.get(uuid=uuid.UUID(action_condition))])
                    
        return action_groups + single_actions

    def get_result(self, action_instance):
        if self.category == Action.Category.EXAMINATION:
            return self.examination_result(
                action_instance.get_patient_examination_codes()
            )
        else:
            return self.generic_result()

    def examination_result(self, examination_codes):
        result_string = f"{self.name} Ergebnis:"
        for examination_type, result_dict in self.results.items():
            current_code = examination_codes.get(examination_type, "")
            result_substring = result_dict.get(current_code)

            if result_substring:
                result_string += f" {examination_type}: {result_substring}"
            else:
                error_message = f"Could not find corresponding value for code {current_code} in {examination_type}"
                logging.error(error_message)
                continue  # skip to avoid crashing

        return result_string

    def generic_result(self):
        return f"{self.name} wurde durchgeführt"

    def __str__(self):
        return f"Action {self.name}"