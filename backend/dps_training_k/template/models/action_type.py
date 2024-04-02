from django.db import models
from django.conf import settings


class ActionType(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=10)
    condition = models.JSONField(null=True, blank=True, default=None)

    def application_status(self, patient, area):
        if (
            settings.IS_PATIENT_TRIAGE_INTEGRATION
        ):  # ToDo: Remove after successfull integration test
            from random import randint

            if randint(0, 1):
                return False, "Randomly declined"
            else:
                return True, None
        return True, None

    def result(self, patient, area):
        return None
