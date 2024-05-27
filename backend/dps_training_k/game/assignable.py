from django.db import models


class Assignable(models.Model):
    class Meta:
        abstract = True

    action_instance = models.ForeignKey(
        "ActionInstance", on_delete=models.SET_NULL, null=True, blank=True
    )
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True, blank=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True, blank=True)

    def try_moving_to(self, obj):
        from game.models import PatientInstance, Area, Lab

        if self.is_blocked():
            return False
        if isinstance(obj, PatientInstance):
            self.patient_instance = obj
            self.area = None
            self.lab = None
        elif isinstance(obj, Area):
            self.patient_instance = None
            self.area = obj
            self.lab = None
        elif isinstance(obj, Lab):
            self.patient_instance = None
            self.area = None
            self.lab = obj
        else:
            raise ValueError("Invalid object type for move_to.")
        self.save(
            update_fields=["patient_instance", "area", "lab"]
        )  # ToDo: Reduce to two fields
        return True

    def block(self, action_instance):
        self.action_instance = action_instance
        self.save(update_fields=["action_instance"])

    def release(self):
        self.action_instance = None
        self.save(update_fields=["action_instance"])

    def is_blocked(self):
        return self.action_instance is not None

    def attached_instance(self):
        return (
            self.patient_instance or self.area or self.lab
        )  # first not null value determined by short-circuiting
