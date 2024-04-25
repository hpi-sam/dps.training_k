from django.db import models
from helpers.models import UUIDable
from .resource import Resource
import json
import uuid


class Action(UUIDable, models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        LAB = "LA", "lab"
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
    success_result = models.JSONField(null=True, blank=True, default=None)

    def consumed_resources(self):
        resources = json.loads(self.conditions)["material"]
        resources = {
            Resource.objects.get(uuid=uuid.UUID(key)): amount
            for key, amount in resources.items()
        }
        return resources

    def produced_resources(self):
        if not "material" in json.loads(self.success_result):
            return None
        resources = json.loads(self.success_result)["material"]
        resources = {
            Resource.objects.get(uuid=uuid.UUID(key)): amount
            for key, amount in resources.items()
        }
        return resources

    def get_result(self, patient_state=None, area_materials=None):
        if self.category == Action.Category.TREATMENT:
            return self.treatment_result(patient_state)
        elif self.category == Action.Category.EXAMINATION:
            return self.examination_result(patient_state)
        elif self.category == Action.Category.LAB:
            return self.lab_result(area_materials)

    def treatment_result(self, patient_state):
        return "This is a treatment result"

    def examination_result(self, patient_state):
        return "This is an examination result"

    def lab_result(self, area_materials):
        return "This is a lab result"

    def application_status(self, patient_instance, area):
        return True, None
