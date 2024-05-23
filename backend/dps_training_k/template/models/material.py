from django.db import models
from helpers.models import UUIDable


class Material(UUIDable, models.Model):
    class Category(models.TextChoices):
        DEVICE = "DE", "Device"
        BLOOD = "BL", "Blood"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=Category.choices, max_length=2)
    is_reusable = models.BooleanField()
