import json
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from helpers.fields_not_null import one_or_more_field_not_null


class ScheduledEvent(models.Model):
    class Meta:
        ordering = ["exercise", "end_date"]

    exercise = models.ForeignKey(
        "Exercise",
        on_delete=models.CASCADE,
        related_name="events",
    )
    end_date = models.DateTimeField()
    kwargs = models.TextField(blank=True, null=True)
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
        **kwargs,
    ):
        try:
            scheduled_event = ScheduledEvent(
                exercise=exercise,
                end_date=cls.calculate_finish_time(t_sim_delta, exercise),
                method_name=method_name,
                kwargs=json.dumps(kwargs),
            )
            scheduled_event.save()
        except TypeError as e:
            raise ValueError(
                "kwargs passed to create_event must be JSON serializable"
            ) from e

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

    @classmethod
    def get_time_until_completion(cls, object):
        from game.models import PatientInstance, ActionInstance, Area, Exercise

        try:
            # Get the related Owner instance
            if isinstance(object, PatientInstance):
                owner_instance = Owner.objects.filter(patient_owner=object).latest("id")
            elif isinstance(object, ActionInstance):
                owner_instance = Owner.objects.filter(
                    action_instance_owner=object
                ).latest("id")
            elif isinstance(object, Exercise):
                owner_instance = Owner.objects.filter(exercise_owner=object).latest(
                    "id"
                )
            elif isinstance(object, Area):
                owner_instance = Owner.objects.filter(area_owner=object).latest("id")
            # Retrieve ScheduledEvent associated with the Owner instance and calculate remaining time
            time_until_event = owner_instance.event.end_date - settings.CURRENT_TIME()
            return int(
                time_until_event.total_seconds()
            )  # would return float if not casted, float isn't necessary here
        except Owner.DoesNotExist:
            # Handle the case where no Owner is associated with the related object, aka there is no scheduled event
            return None

    @classmethod
    def remove_events_of_exercise(cls, exercise):
        cls.objects.filter(exercise=exercise).delete()

    def action(self):
        owner_instance = self.owner.owner_instance()
        method = getattr(owner_instance, self.method_name)
        if self.kwargs:
            kwargs = json.loads(self.kwargs)
            method(**kwargs)
        else:
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
            one_or_more_field_not_null(
                [
                    "patient_owner",
                    "exercise_owner",
                    "area_owner",
                    "action_instance_owner",
                ],
                "owner",
            )
        ]

    event = models.OneToOneField(
        "ScheduledEvent",
        on_delete=models.CASCADE,
    )

    action_instance_owner = models.ForeignKey(
        "ActionInstance",
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
    exercise_owner = models.ForeignKey(
        "Exercise",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )
    patient_owner = models.ForeignKey(
        "PatientInstance",
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
            raise Exception("This owner instance was created without an actual owner")


@receiver(post_delete, sender=Owner)
def delete_patient(sender, instance, **kwargs):
    if instance.event:
        instance.event.delete()
