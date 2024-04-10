from django.db import models


class Action(models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        DIAGNOSIS = "DI", "diagnosis"

    name = models.CharField(max_length=100)
    category = models.CharField(choices=Category.choices, max_length=2)
    duration = models.IntegerField(
        default=10,
        help_text="Duration in seconds in realtime. Might be scaled by external factors.",
    )
    conditions = models.JSONField(null=True, blank=True, default=None)
