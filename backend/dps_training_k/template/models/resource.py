from django.db import models
from helpers.models import UUIDable


class Resource(UUIDable, models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_returnable = models.BooleanField()
