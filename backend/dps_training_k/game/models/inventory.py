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
        InventoryEntryDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def change(self, net_change):
        # ToDo: Uncomment once condition checks are implemented
        # if -net_change > self.amount:
        #    raise ValueError(
        #        f"Not enough resources {self.resource.name} to perform this action- might have happened because of a race condition"
        #    )
        self.amount += net_change
        self.save(update_fields=["amount"])
        return self.amount


class Inventory(models.Model):
    def get_owner(self):
        from game.models import Area, Lab, PatientInstance

        if PatientInstance.objects.filter(inventory=self):
            return PatientInstance.objects.get(inventory=self)
        elif Lab.objects.filter(inventory=self):
            return Lab.objects.get(inventory=self)
        elif Area.objects.filter(inventory=self):
            return Area.objects.get(inventory=self)
        raise ValueError("Inventory does not have an owner")

    def resource_stock(self, resource):
        try:
            entry = self.entries.get(resource=resource)
            return entry.amount
        except self.entries.model.DoesNotExist:
            return 0

    def change_resource(self, resource, net_change):
        entry, _ = InventoryEntry.objects.get_or_create(
            inventory=self, resource=resource
        )
        return entry.change(net_change)

    def transition_resource_to(self, inventory, resource, net_change):
        if net_change < 0:
            raise ValueError(
                "Transitioning resources to another inventory requires a positive net change"
            )
        self.change_resource(resource, -net_change)
        inventory.change_resource(resource, net_change)
