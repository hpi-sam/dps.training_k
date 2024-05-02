from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def start_examination(self, action_template, patient_instance):
        from game.models import LabActionInstance

        action_instance = LabActionInstance.create(
            action_template, self, patient_instance=patient_instance
        )
        action_instance.try_application()
        return action_instance

    def start_production(self, action_template, area):
        from game.models import LabActionInstance

        action_instance = LabActionInstance.create(action_template, self, area=area)
        action_instance.try_application()
        return action_instance
