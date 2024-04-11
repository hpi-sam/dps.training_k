from django.db import models


class Action(models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        LAB = "LA", "lab"
        OTHER = "OT", "other"

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    category = models.CharField(choices=Category.choices, max_length=2)
    duration = models.IntegerField(
        default=10,
        help_text="Duration in seconds in realtime. Might be scaled by external factors.",
    )
    conditions = models.JSONField(null=True, blank=True, default=None)

    def application_status(self, patient, area):
        return True, None
