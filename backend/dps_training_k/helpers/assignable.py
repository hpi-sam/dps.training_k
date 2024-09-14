from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from helpers import exactly_one_field_not_null


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

    # GenericForeignKey is just a virtual field for unified access, only _content_type and _object_id are actually stored in DB
    moved_from_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    moved_from_object_id = models.PositiveIntegerField(null=True, blank=True)
    moved_from = GenericForeignKey("moved_from_content_type", "moved_from_object_id")

    def __init_subclass__(cls, **kwargs):
        """Create a unique name for each constraint for subclasses of Assignable."""
        super().__init_subclass__(**kwargs)
        constraint_name = (
            f"assignable_{cls.__name__.lower()}_exactly_one_field_not_null"
        )
        cls._meta.constraints.append(
            exactly_one_field_not_null(
                ["patient_instance", "area", "lab"], constraint_name
            )
        )

    def _perform_move(self, obj):
        from game.models import PatientInstance, Area, Lab

        self.moved_from = self.attached_instance()

        if isinstance(obj, PatientInstance):
            if self.patient_instance is obj:
                return False
            self.patient_instance = obj
            self.area = None
            self.lab = None
        elif isinstance(obj, Area):
            if self.area is obj:
                return False
            self.patient_instance = None
            self.area = obj
            self.lab = None
        elif isinstance(obj, Lab):
            if self.lab is obj:
                return False
            self.patient_instance = None
            self.area = None
            self.lab = obj

        self.save(
            update_fields=[
                "patient_instance",
                "area",
                "lab",
                "moved_from_content_type",
                "moved_from_object_id",
            ]
        )
        return True, ""

    @staticmethod
    def can_move_to_type(obj):
        from game.models import PatientInstance, Area, Lab

        return isinstance(obj, (PatientInstance, Area, Lab))

    def is_blocked(self):
        return self.action_instance is not None

    def attached_instance(self):
        # First non-null value determined by short-circuiting
        return self.patient_instance or self.area or self.lab

    def block(self, action_instance):
        self.action_instance = action_instance
        self.save(update_fields=["action_instance"])

    def release(self):
        self.action_instance = None
        self.save(update_fields=["action_instance"])
