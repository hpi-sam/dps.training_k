from django.db import models


class Lab(models.Model):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def start_examination(self, action_template, patient_instance):
        pass

    def start_production(self, action_template, area):
        pass

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
