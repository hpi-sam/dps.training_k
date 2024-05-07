from django.db import models
from game.channel_notifications import MaterialInstanceDispatcher
from template.models.material import Material


class MaterialInstance(models.Model):
    material_template = models.ForeignKey("template.Material", on_delete=models.CASCADE)
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        MaterialInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

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

    @classmethod
    def generate_materials(cls, materials_recipe, area):
        for material_uuid, amount in materials_recipe.items():
            for _ in range(amount):
                material_template = Material.objects.get(uuid=material_uuid)
                cls.objects.create(material_template=material_template, area=area)

    def block(self):
        self.is_blocked = True
        self.save(update_fields=["is_blocked"])

    def release(self):
        self.is_blocked = False
        self.save(update_fields=["is_blocked"])
