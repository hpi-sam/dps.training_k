from abc import abstractmethod
from typing import List

from django.db import models

import game.models.material_instance as mi
import game.models.personnel as p


class MoveableTo(models.Model):
    class Meta:
        abstract = True

    def material_assigned(self, material_template) -> List["mi.MaterialInstance"]:
        return list(self.materialinstance_set.filter(template=material_template))

    def material_available(self, material_template) -> List["mi.MaterialInstance"]:
        return list(
            self.materialinstance_set.filter(
                template=material_template, action_instance=None
            )
        )

    def personnel_assigned(self) -> List["p.Personnel"]:
        return list(self.personnel_set.all())

    def personnel_available(self) -> List["p.Personnel"]:
        return list(self.personnel_set.filter(action_instance=None))

    @staticmethod
    @abstractmethod
    def frontend_model_name():
        pass
