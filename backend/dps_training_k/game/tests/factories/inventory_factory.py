import factory
from game.models import Inventory, InventoryEntry
from template.tests.factories.resource_factory import (
    ResourceFactory,
)


class InventoryEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryEntry
        django_get_or_create = ("inventory", "resource", "amount")

    inventory = factory.SubFactory("game.tests.factories.EmptyInventoryFactory")
    resource = factory.SubFactory("template.tests.factories.ResourceFactory")
    amount = 0


class EmptyInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory
        django_get_or_create = ("area", "lab")

    area = factory.SubFactory("game.tests.factories.AreaFactory")
    lab = None


class FilledInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory
        django_get_or_create = ("area", "lab")

    area = factory.SubFactory("game.tests.factories.AreaFactory")
    lab = None
    # @factory.post_generation
    # def generate_inventory_entries(self, create, extracted, **kwargs):
    #    if not create:
    #        return
    #    InventoryEntryFactory(inventory=self, resource=ResourceFactory(), amount=1)
