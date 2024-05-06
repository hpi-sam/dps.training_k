from django.db import models


class MaterialInstance(models.Model):
    material_template = models.ForeignKey("template.Material", on_delete=models.CASCADE)
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True)
    is_blocked = models.BooleanField(default=False)

    def try_moving_to(self, obj):
        if self.is_blocked:
            return False
        if isinstance(obj, models.PatientInstance):
            self.patient_instance = obj
            self.area = None
            self.lab = None
        elif isinstance(obj, models.Area):
            self.patient_instance = None
            self.area = obj
            self.lab = None
        elif isinstance(obj, models.Lab):
            self.patient_instance = None
            self.area = None
            self.lab = obj
        else:
            raise ValueError("Invalid object type for move_to.")
        self.save(
            update_fields=["patient_instance", "area", "lab"]
        )  # ToDo: Reduce to two fields
        return True
