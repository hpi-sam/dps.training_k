from abc import abstractmethod

from django.core.exceptions import ImproperlyConfigured
from django.db import models


class Moveable(models.Model):
    """Abstract class for objects that can be moved to other objects. Must have a 'name' attribute."""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_name_attribute_exists()

    def check_name_attribute_exists(self):
        """Ensure that the name attribute is implemented (either as property or field)."""
        if not hasattr(self, "name"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must have a 'name' attribute to inherit Moveable."
            )

    def try_moving_to(self, obj) -> tuple[bool, str]:
        """Returns whether the object was moved successfully and an error message if not."""
        from helpers.moveable_to import MoveableTo

        if not isinstance(obj, MoveableTo):
            raise TypeError(
                f"Object must inherit from MoveableTo, got {type(obj).__name__} instead."
            )

        if self.is_blocked():
            # noinspection PyUnresolvedReferences
            return False, f"{self.name} ist blockiert und kann nicht verlegt werden."
        if not self.can_move_to(obj):
            # frontend_model_name is defined in moveable_to
            # noinspection PyUnresolvedReferences
            return (
                False,
                f"{self.name} kann nicht zu Objekten des Typs {obj.frontend_model_name()} verlegt werden.",
            )
        return self.perform_move(obj)

    @abstractmethod
    def is_blocked(self):
        pass

    @staticmethod
    @abstractmethod
    def can_move_to_type(obj):
        pass

    @abstractmethod
    def _perform_move(self, obj) -> tuple[bool, str]:
        """Move the object to another object. The string can be used for either error or warning messages for the frontend."""
        # prone to race conditions, we don't care as highly unlikely
        pass

    @abstractmethod
    def attached_instance(self):
        """Return the instance this object was moved to."""
        pass
