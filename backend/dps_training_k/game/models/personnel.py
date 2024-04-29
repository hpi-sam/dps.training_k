from django.db import models

from game.channel_notifications import PersonnelDispatcher


class Personnel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    area = models.ForeignKey("Area", on_delete=models.CASCADE, related_name="personnel")
    assigned_patient = models.ForeignKey(
        "PatientInstance", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Personnel #{self.id} called {self.name} in area {self.area.name}"

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        PersonnelDispatcher.save_and_notify(self, update_fields, *args, **kwargs)
        if self.name == "":
            self.name = f"Personnel {self.id}"
            self.save(update_fields=["name"])

    def delete(self, using=None, keep_parents=False):
        PersonnelDispatcher.delete_and_notify(self)
