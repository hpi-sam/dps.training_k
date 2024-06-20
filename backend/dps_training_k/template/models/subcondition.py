from django.db import models

class Subcondition(models.Model):
    name = models.CharField(max_length=100)
    upper_limit = models.IntegerField()
    lower_limit = models.IntegerField()
    fulfilling_measures = models.JSONField()

    def __str__(self):
        return f"Subcondition {self.name}"