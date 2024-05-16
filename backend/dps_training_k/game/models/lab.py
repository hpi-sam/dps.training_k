from django.db import models


class Lab(models.Model):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def material_assigned(self, material_template):
        return self.material_set.filter(material_template=material_template)

    def material_available(self, material_template):
        return self.material_set.filter(
            material_template=material_template, is_blocked=False
        )

    def personel_assigned(self):
        return None

    def personnel_available(self):
        return None

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
