from abc import abstractmethod
from typing import List

from django.core.exceptions import ImproperlyConfigured
from django.db import models

import game.models.material_instance as mi
import game.models.personnel as p


class MoveableTo(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_name_attribute()

    def check_name_attribute(self):
        """Ensure that the name attribute is implemented (either as property or field)."""
        if not hasattr(self, "name"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have a 'name' attribute to inherit Moveable."
            )

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
