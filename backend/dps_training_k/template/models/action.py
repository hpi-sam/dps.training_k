from django.db import models
from .material import Material
from helpers.models import UUIDable
import json, uuid


class Action(UUIDable, models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        LAB = "LA", "lab"
        PRODUCTION = "PR", "production"
        OTHER = "OT", "other"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=Category.choices, max_length=2)
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
        results = json.loads(self.results)
        if not "produced_material" in results:
            return None
        resources = results["produced_material"]
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
            return None
        parsed_condition = json.loads(self.conditions)
        if not "material" in parsed_condition:
            return None
        material_uuids = parsed_condition["material"]
        needed_material_groups = []
        for material_condition_uuid in material_uuids:
            if material_condition_uuid is list:
                needed_material_group = [
                    Material.objects.get(uuid=uuid.UUID(uuid))
                    for uuid in material_condition_uuid
                ]
                needed_material_groups.append(needed_material_group)
        needed_single_material = [
            [Material.objects.get(uuid=uuid.UUID(uuid))]
            for uuid in material_uuids
            if uuid is not list
        ]
        return needed_material_groups + needed_single_material

    def personnel_count__needed(self):
        if not self.conditions:
            return None
        parsed_condition = json.loads(self.conditions)
        if not "num_personnel" in parsed_condition:
            return None
        return parsed_condition["num_personnel"]

    def ckeck_conditions_and_suggest_blocking(self, material_owner, personell_owner):
        """
        Iff all conditions are met, it suggests which objects to use for this action.
        Every argument passed needs to return a queryset for their "available"-like methods.
        This method does not interact with the objects of the queryset, so it makes no assumptions about them
        :params material_owner: Instance having a material_available method
        :params personell_owner: Instance having a personell_available method
        :return bool, list of objects, str: True if all conditions are met, False if not.
        If True, the list contains all resources the condition wants to use.
        If false, send a string describing the reason
        """
        resources_to_block = []
        for material_condition_or in self.template.material_needed():
            for material_condition in material_condition_or:
                available_materials = material_owner.material_available(
                    material_condition
                )
                if available_materials:
                    resources_to_block.append(available_materials[0])
                    break
                else:
                    return (
                        False,
                        None,
                        f"A material of the materials {material_condition} is needed but not available.",
                    )

        available_personnel = personell_owner.personell_available()
        if available_personnel.count() < self.template.personnel_count__needed():
            return (
                False,
                None,
                f"{self.template.personnel_count__needed()} personnel are needed but only {available_personnel.count()} are available.",
            )
        for i in range(self.template.personnel_count__needed()):
            resources_to_block.append(available_personnel[i])
        return True, resources_to_block, None

    def get_result(self, patient_state_data=None, area_materials=None):
        if self.category == Action.Category.TREATMENT:
            return self.treatment_result(patient_state_data)
        elif self.category == Action.Category.EXAMINATION:
            return self.examination_result(patient_state_data)
        elif self.category == Action.Category.LAB:
            return self.lab_result(area_materials)
        elif self.category == Action.Category.PRODUCTION:
            return self.production_result()

    def treatment_result(self, patient_state):
        return f"Behandlung {self.name} wurde durchgeführt"

    def examination_result(self, patient_state_data):
        result_string = f"{self.name} Ergebnis:"
        # iterate through result map
        results = json.loads(self.results)
        for key, values in results.items():
            # find correct result code for this patient
            result_code = json.loads(patient_state_data)[key]
            # find string value corresponding to result code
            found = False
            for value in values:
                if result_code in value:
                    result_string += f" {key}: {value[result_code]}"
                    found = True
            if not found:
                raise ValueError(
                    "Examination result: Couldn't find corresponding value for result code"
                )

        return result_string

    def production_result(self):
        return f"{self.name} wurde durchgeführt"

    def lab_result(self, area_materials):
        return "This is a lab result"
