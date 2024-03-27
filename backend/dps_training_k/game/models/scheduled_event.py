from django.db import models
from django.conf import settings
from datetime import timedelta
from helpers.one_field_not_null import OneFieldNotNull


class ScheduledEvent(models.Model):
    class Meta:
        ordering = ["exercise", "end_date"]

    exercise = models.ForeignKey(
        "Exercise",
        on_delete=models.CASCADE,
        related_name="events",
    )
    end_date = models.DateTimeField()
    method_name = models.CharField(max_length=100)

    @classmethod
    def create_event(cls, exercise, t_sim_delta, method_name, patient=None, area=None):
        scheduled_event = ScheduledEvent(
            exercise=exercise,
            end_date=cls.calculate_finish_time(t_sim_delta, exercise),
            method_name=method_name,
        )
        scheduled_event.save()
        Owner.create_owner(scheduled_event, patient=patient, area=area)

    @classmethod
    def calculate_finish_time(cls, t_sim_delta, exercise):
        deltatime = timedelta(seconds=t_sim_delta * exercise.time_factor())
        return settings.CURRENT_TIME() + deltatime

    def action(self):
        owner_instance = self.owner.owner_instance()
        method = getattr(owner_instance, self.method_name)
        method()
        self.delete()

    def __str__(self):
        owner_instance = self.owner.owner_instance()
        return f"ScheduledEvent #{self.id}, model name {owner_instance.__class__.__name__}, instance #{owner_instance}, exercise #{self.exercise}, trigger on: {self.end_date}"


class Owner(OneFieldNotNull, models.Model):
    event = models.OneToOneField(
        "ScheduledEvent",
        on_delete=models.CASCADE,
        related_name="owner",
    )
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
    def create_owner(cls, event, patient=None, exercise=None, area=None):
        # patient always needs to be checked before exercise, as exercise and patient are being passed when patient creates scheduled event
        if patient:
            return cls.objects.create(event=event, patient_owner=patient)
        elif area:
            # return cls.objects.create(event=event, area_owner=area)
            pass
        elif exercise:
            return cls.objects.create(event=event, exercise_owner=exercise)
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
