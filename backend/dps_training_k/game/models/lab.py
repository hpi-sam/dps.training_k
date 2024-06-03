from django.db import models

from helpers.moveable_to import MoveableTo
from game.models import MaterialInstance
from template.models import Material
from template.constants import MaterialIDs


class Lab(MoveableTo):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def create_basic_devices(self):
        lab_materials = Material.objects.filter(is_lab=True).exclude(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE
        )
        for material in lab_materials:
            MaterialInstance.objects.update_or_create(template=material, lab=self)
        for _ in range(4):
            MaterialInstance.objects.create(
                template=Material.objects.get(
                    uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE
                ),
                lab=self,
            )

    @property
    def name(self):
        return self.exercise.frontend_id

    def can_receive_actions(self):
        return True

    @staticmethod
    def frontend_model_name():
        return "Labor"

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
