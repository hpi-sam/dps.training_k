import uuid
from django.db import models


class UUIDable(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
