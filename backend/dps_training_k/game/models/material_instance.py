from django.db import models


class MaterialInstance(models.Model):
    material_template = models.ForeignKey("template.Material", on_delete=models.CASCADE)
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True)
    is_blocked = models.BooleanField(default=False)

