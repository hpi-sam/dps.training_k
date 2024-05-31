from django.db import models

from game.channel_notifications import MaterialInstanceDispatcher
from helpers.assignable import Assignable
from helpers.moveable import Moveable


class MaterialInstance(Assignable, Moveable, models.Model):

    template = models.ForeignKey("template.Material", on_delete=models.CASCADE)

    @property
    def name(self):
        return self.template.name

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        MaterialInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def delete(self, using=None, keep_parents=False):
        MaterialInstanceDispatcher.delete_and_notify(self)

    @property
    def is_reusable(self):
        return self.template.reusable

    @classmethod
    def generate_materials(cls, materials_recipe, area):
        for template, amount in materials_recipe.items():
            for _ in range(amount):
                cls.objects.create(template=template, area=area)

    def consume(self):
        self.delete()

    def __str__(self):
        return f"{self.name} ({self.id}) assigned to {self.attached_instance()}"
