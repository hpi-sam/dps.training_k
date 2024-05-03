from django.db import models
from django.conf import settings
from datetime import timedelta
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
            patient_action_instance=patient_action_instance,
            lab_action_instance=lab_action_instance,
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
            raise Exception("This owner instance was created  without and actual owner")
