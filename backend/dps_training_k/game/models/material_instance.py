from django.db import models

from game.channel_notifications import MaterialInstanceDispatcher
from helpers.one_or_more_field_not_null import one_or_more_field_not_null


class MaterialInstance(models.Model):
    class Meta:
        constraints = [
            one_or_more_field_not_null(["patient_instance", "area", "lab"], "material")
        ]

    action_instance = models.ForeignKey(
        "ActionInstance", on_delete=models.CASCADE, null=True, blank=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True, blank=True)
    material_template = models.ForeignKey("template.Material", on_delete=models.CASCADE)
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True, blank=True
    )

    @property
    def name(self):
        return self.material_template.name

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        MaterialInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def delete(self, using=None, keep_parents=False):
        MaterialInstanceDispatcher.delete_and_notify(self)

    @property
    def is_reusable(self):
        return self.material_template.is_reusable

    @classmethod
    def generate_materials(cls, materials_recipe, area):
        for material_template, amount in materials_recipe.items():
            for _ in range(amount):
                cls.objects.create(material_template=material_template, area=area)

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

    def consume(self):
        self.delete()

    def attached_instance(self):
        return (
            self.patient_instance or self.area or self.lab
        )  # first not null value determined by short-circuiting

    def __str__(self):
        return f"{self.name} ({self.id})"
