from django.db import models


class Action(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=10)
    condition = models.JSONField(null=True, blank=True, default=None)
