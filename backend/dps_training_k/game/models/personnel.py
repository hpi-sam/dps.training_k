from django.db import models

from game.assignable import Assignable
from game.channel_notifications import PersonnelDispatcher


class Personnel(Assignable):

    name = models.CharField(max_length=100, blank=True)

    @classmethod
    def create_personnel(cls, area, name):
        unique_name = name
        number = 1

        # Loop until a unique name is found
        while cls.objects.filter(
            name=unique_name, area__exercise=area.exercise
        ).exists():
            unique_name = f"{name} {number}"
            number += 1

        return cls.objects.create(
            area=area,
            name=unique_name,
        )

    def delete(self, using=None, keep_parents=False):
        PersonnelDispatcher.delete_and_notify(self)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        PersonnelDispatcher.save_and_notify(
            self, update_fields, super(), *args, **kwargs
        )

    def __str__(self):
        return f"{self.name} ({self.id}) assigned to {self.attached_instance()}"
