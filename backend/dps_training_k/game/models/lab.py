from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def start_examination(self, action_template, patient_instance):
        pass

    def start_production(self, action_template, area):
        pass
