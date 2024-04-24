from django.db import models


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
    amount = models.IntegerField()

    def change(self, net_change):
        if -net_change > self.amount:
            raise ValueError(
                "Not enough resources - might have happened because of a race condition"
            )
        self.amount += net_change
        self.save(update_fields=["amount"])
        return self.amount


class Inventory(models.Model):
    area = models.OneToOneField(
        "Area", on_delete=models.CASCADE, related_name="consuming_inventory"
    )

    def resource_stock(self, resource):
        return self.entries.filter(resource=resource).count()

    def change_resource(self, resource, net_change):
        entry = self.entries.filter(resource=resource).first()
        return entry.change(net_change)
