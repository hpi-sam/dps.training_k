from django.db import models


class Lab(models.Model):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def material_assigned(self, material_template):
        return list(self.material_set.filter(template=material_template))

    def material_available(self, material_template):
        return list(
            self.material_set.filter(template=material_template, action_instance=None)
        )

    def personel_assigned(self):
        return []

    def personnel_available(self):
        return []

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
