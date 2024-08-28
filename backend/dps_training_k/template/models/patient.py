from django.db import models


class Patient(models.Model):
    info = models.JSONField()
    flow = models.JSONField()
    states = models.JSONField()
    transitions = models.JSONField()
    components = models.JSONField()

    def __str__(self):
        return f"Patient {self.info.get('code')}"