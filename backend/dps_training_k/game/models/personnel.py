from django.db import models

from game.channel_notifications import PersonnelDispatcher


class Personnel(models.Model):

    action_instance = models.ForeignKey(
        "game.ActionInstance", on_delete=models.SET_NULL, null=True, blank=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE)
    assigned_patient = models.ForeignKey(
        "PatientInstance", on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100, blank=True)

    def delete(self, using=None, keep_parents=False):
        PersonnelDispatcher.delete_and_notify(self)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        PersonnelDispatcher.save_and_notify(
            self, update_fields, super(), *args, **kwargs
        )
        if self.name == "":
            self.name = f"Personnel {self.id}"
            self.save(update_fields=["name"])

    def block(self, action_instance):
        self.action_instance = action_instance
        self.save(update_fields=["action_instance"])

    def release(self):
        self.action_instance = None
        self.save(update_fields=["action_instance"])

    def is_blocked(self):
        return self.action_instance is not None

    def __str__(self):
        return f"Personnel #{self.id} called {self.name} in area {self.area.name}"
