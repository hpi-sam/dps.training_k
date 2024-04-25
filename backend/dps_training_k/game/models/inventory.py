from django.db import models
from django.db.models import CheckConstraint, Q


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
            CheckConstraint(
                check=Q(area__isnull=False) | Q(lab__isnull=False),
                name="at_least_one_field_not_null",
            ),
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
