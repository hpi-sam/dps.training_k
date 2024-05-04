import json
from datetime import timedelta

from django.conf import settings
from django.db import models

from helpers.one_field_not_null import one_or_more_field_not_null


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
    kwargs = models.TextField(blank=True, null=True)

    @classmethod
    def create_event(
        cls,
        exercise,
        t_sim_delta,
        method_name,
        patient=None,
        area=None,
        patient_action_instance=None,
        lab_action_instance=None,
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
            patient_action_instance=patient_action_instance,
            lab_action_instance=lab_action_instance,
        )

    @classmethod
    def calculate_finish_time(cls, t_sim_delta, exercise):
        deltatime = timedelta(seconds=t_sim_delta * exercise.time_factor())
        return settings.CURRENT_TIME() + deltatime

    @classmethod
    def get_time_until_completion(cls, object):
        from game.models import PatientInstance, Area, Exercise

        try:
            # Get the related Owner instance
            if isinstance(object, PatientInstance):
                owner_instance = Owner.objects.filter(patient_owner=object).latest("id")
            elif isinstance(object, PatientActionInstance):
                owner_instance = Owner.objects.filter(
                    patient_action_instance_owner=object
                ).latest("id")
            elif isinstance(object, LabActionInstance):
                owner_instance = Owner.objects.filter(
                    lab_action_instance_owner=object
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
                    "patient_action_instance_owner",
                    "lab_action_instance_owner",
                ],
                "owner",
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

    patient_action_instance_owner = models.ForeignKey(
        "PatientActionInstance",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )

    lab_action_instance_owner = models.ForeignKey(
        "LabActionInstance",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_events",
    )

    @classmethod
    def create_owner(
        cls,
        event,
        patient=None,
        exercise=None,
        area=None,
        patient_action_instance=None,
        lab_action_instance=None,
    ):
        not_none_not_exercise_fields = [
            patient,
            area,
            patient_action_instance,
            lab_action_instance,
        ]
        if exercise and len(
            not_none_not_exercise_fields
        ) - not_none_not_exercise_fields.count(
            None
        ):  # remove default exercise when other owner is set
            exercise = None
        return cls.objects.create(
            event=event,
            patient_owner=patient,
            exercise_owner=exercise,
            area_owner=area,
            patient_action_instance_owner=patient_action_instance,
            lab_action_instance_owner=lab_action_instance,
        )

    def owner_instance(self):
        if self.patient_owner:
            return self.patient_owner
        elif self.exercise_owner:
            return self.exercise_owner
        elif self.area_owner:
            return self.area_owner
        elif self.patient_action_instance_owner:
            return self.patient_action_instance_owner
        elif self.lab_action_instance_owner:
            return self.lab_action_instance_owner
        else:
            raise Exception("This owner instance was created without an actual owner")
