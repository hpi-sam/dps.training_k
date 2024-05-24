from django.core.exceptions import ImproperlyConfigured


class Assignable:

    def save(self, *args, **kwargs):
        # hasattr -> checks if the object has all needed fields.
        if (
            not hasattr(self, "action_instance")
            or not hasattr(self, "patient_instance")
            or not hasattr(self, "area")
            or not hasattr(self, "lab")
        ):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must define all necessary assignable fields."
            )
        super().save(*args, **kwargs)

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

    def attached_instance(self):
        return (
            self.patient_instance or self.area or self.lab
        )  # first not null value determined by short-circuiting
