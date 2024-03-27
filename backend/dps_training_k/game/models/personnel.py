from django.db import models


class Personnel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    area = models.ForeignKey("Area", on_delete=models.CASCADE)

    def __str__(self):
        return f"Personnel #{self.id} called {self.name} in area {self.area.name}"

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            self.name = f"Personnel {self.id}"
            super().save(update_fields=["name"])
