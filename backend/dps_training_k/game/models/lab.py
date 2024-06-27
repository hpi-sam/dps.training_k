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

    def get_completed_action_types(self):
        from game.models import ActionInstanceState
        action_instances = self.actioninstance_set.select_related("template").all()
        applied_actions = set()
        for action_instance in action_instances:
            if action_instance.current_state.name in ActionInstanceState.completion_states():
                applied_actions.add(action_instance.template)
        return applied_actions

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
