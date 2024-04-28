from django.db import models
from helpers.one_field_not_null import one_or_more_field_not_null
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
        constraints = [
            one_or_more_field_not_null(["area", "lab", "patient"], "inventory"),
        ]

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
        "PatientInstance",
        on_delete=models.CASCADE,
        related_name="consumning_inventory",
        blank=True,
        null=True,
    )

    def resource_stock(self, resource):
        entry = self.entries.get(resource=resource)
        if entry is None:
            return 0
        return entry.amount

    def change_resource(self, resource, net_change):
        entry, _ = InventoryEntry.objects.get_or_create(
            inventory=self, resource=resource
        )
        return entry.change(net_change)

    def transition_resource_to(self, Inventory, resource, net_change):
        if net_change < 0:
            raise ValueError(
                "Transitioning resources to another inventory requires a positive net change"
            )
        self.change_resource(resource, -net_change)
        Inventory.change_resource(resource, net_change)
