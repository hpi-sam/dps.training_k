from django.db import models


class Personnel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    area = models.ForeignKey("Area", on_delete=models.CASCADE)
    assigned_patient = models.ForeignKey(
        "PatientInstance", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Personnel #{self.id} called {self.name} in area {self.area.name}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = f"Personnel {self.id}"
        super().save(*args, **kwargs)
