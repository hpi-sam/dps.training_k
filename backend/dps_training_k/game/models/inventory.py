from django.db import models
from helpers.x_fields_not_null import x_fields_not_null
from game.channel_notifications import InventoryEntryDispatcher


class InventoryEntry(models.Model):
    resource = models.ForeignKey(
        "template.Resource",
        on_delete=models.CASCADE,
    )
    inventory = models.ForeignKey(
        "Inventory",
        on_delete=models.CASCADE,
        related_name="entries",
    )
    amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        InventoryEntryDispatcher.save_and_notify(self, changes, *args, **kwargs)

    def change(self, net_change):
        # ToDo: Uncomment once condition checks are implemented
        # if -net_change > self.amount:
        #    raise ValueError(
        #        "Not enough resources - might have happened because of a race condition"
        #    )
        self.amount += net_change
        self.save(update_fields=["amount"])
        return self.amount


class Inventory(models.Model):

    class Meta:
        constraints = [x_fields_not_null(1, ["area", "lab", "patient"])]

    area = models.OneToOneField(
        "Area",
        on_delete=models.CASCADE,
        related_name="consuming_inventory",
        blank=True,
        null=True,
    )
    lab = models.OneToOneField(
        "Lab",
        on_delete=models.CASCADE,
        related_name="consuming_inventory",
        blank=True,
        null=True,
    )
    patient = models.OneToOneField(
        "Patient",
        on_delete=models.CASCADE,
        related_name="consumning_inventory",
        blank=True,
        null=True,
    )

    def resource_stock(self, resource):
        entries = self.entries.filter(resource=resource)
        if entries.count() > 1:
            raise ValueError("Multiple entries for the same resource")
        if entries.count() == 0:
            return 0
        return entries.first().amount

    def change_resource(self, resource, net_change):
        entry, _ = InventoryEntry.objects.get_or_create(
            inventory=self, resource=resource
        )
        return entry.change(net_change)
