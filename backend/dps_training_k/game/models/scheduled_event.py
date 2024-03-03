from django.db import models
from django.conf import settings


class ScheduledEvent(models.Model):
    class Meta:
        ordering = ["exercise", "date"]

    exercise = models.ForeignKey(
        "Exercise",
        on_delete=models.CASCADE,
        related_name="events",
    )
    date = models.DateTimeField()
    owner = models.OneToOneField(
        "Owner",
        on_delete=models.CASCADE,
        related_name="event",
    )
    method_name = models.CharField(max_length=100)

    @classmethod
    def create_event(cls, exercise, t_sim_delta, method_name, patient=None, area=None):
        cls.objects.create(
            exercise=exercise,
            date=cls.calculate_finish_time(t_sim_delta, exercise),
            owner=Owner.create_owner(patient=patient, exercise=exercise),
            method_name=method_name,
        )

    @classmethod
    def calculate_finish_time(cls, t_sim_delta, exercise):
        return settings.CURRENT_SECONDS() + t_sim_delta * exercise.time_factor()

    def action(self):
        owner_instance = self.owner.owner_instance()
        method = getattr(owner_instance, self.method_name)
        method()
        self.delete()

    def __str__(self):
        owner_instance = self.owner.owner_instance()
        return f"ScheduledEvent #{self.id}, model name {owner_instance.__class__.__name__}, instance #{owner_instance}, exercise #{self.exercise}, trigger on: {self.date}"


class Owner(models.Model):
    patient_owner = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )
    exercise_owner = models.ForeignKey(
        "Exercise",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )

    # area_owner = models.ForeignKey("Area", on_delete=models.CASCADE)

    @classmethod
    def create_owner(cls, patient=None, exercise=None, area=None):
        if patient:
            return cls.objects.create(patient_owner=patient)
        elif area:
            # return cls.objects.create(area_owner=area)
            pass
        elif exercise:
            return cls.objects.create(exercise_owner=exercise)
        else:
            raise Exception("Owner must have a patient or exercise")

    def owner_instance(self):
        if self.patient_owner:
            return self.patient_owner
        elif self.exercise_owner:
            return self.exercise_owner
        # elif self.area_owner:
        #    return self.area_owner
        else:
            return None
