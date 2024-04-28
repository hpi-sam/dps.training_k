from django.db import models
from django.conf import settings
from datetime import timedelta
from backend.dps_training_k.helpers.x_fields_not_null import x_fields_not_null


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
    def create_event(
        cls,
        exercise,
        t_sim_delta,
        method_name,
        patient=None,
        area=None,
        action_instance=None,
    ):
        scheduled_event = ScheduledEvent(
            exercise=exercise,
            end_date=cls.calculate_finish_time(t_sim_delta, exercise),
            method_name=method_name,
        )
        scheduled_event.save()
        Owner.create_owner(
            scheduled_event,
            exercise=exercise,
            patient=patient,
            area=area,
            action_instance=action_instance,
        )

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


class Owner(models.Model):
    """Wrapper model to avoid using GenericForeignKeys as recommended here:
    https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/"""

    class Meta:
        constraints = [
            x_fields_not_null(
                1,
                [
                    "patient_owner",
                    "exercise_owner",
                    "area_owner",
                    "action_instance_owner",
                ],
            )
        ]

    event = models.OneToOneField(
        "ScheduledEvent",
        on_delete=models.CASCADE,
    )
    patient_owner = models.ForeignKey(
        "Patientinstance",
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

    area_owner = models.ForeignKey(
        "Area",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )

    action_instance_owner = models.ForeignKey(
        "ActionInstance",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )

    @classmethod
    def create_owner(
        cls, event, patient=None, exercise=None, area=None, action_instance=None
    ):
        # exercise needs to be checked last, as it is always passed to check for the time factor
        if patient:
            return cls.objects.create(event=event, patient_owner=patient)
        elif area:
            return cls.objects.create(event=event, area_owner=area)
        elif action_instance:
            return cls.objects.create(
                event=event, action_instance_owner=action_instance
            )
        elif exercise:
            return cls.objects.create(event=event, exercise_owner=exercise)
        else:
            raise ValueError("Owner must have a patient or exercise")

    def owner_instance(self):
        if self.patient_owner:
            return self.patient_owner
        elif self.exercise_owner:
            return self.exercise_owner
        elif self.area_owner:
            return self.area_owner
        elif self.action_instance_owner:
            return self.action_instance_owner
        else:
            raise Exception("This owner instance was created  without and actual owner")
