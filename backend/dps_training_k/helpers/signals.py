# ToDo: Adapt online code, import in Channels
from django.dispatch import Signal
from django.db import models

post_update = Signal()


class SignalingQuerySet(models.query.QuerySet):
    def update(self, kwargs):
        super().update(kwargs)
        post_update.send(sender=self.model)


class UpdateSignalManager(models.Manager):
    def getqueryset(self):
        return SignalingQuerySet(self.model, using=self._db)


class UpdateSignals(models.Model):
    """
    When using this class signals will be send when calling the Foo.objects.update() method.
    To decrease coupling we encourage to always use the update method when changing fields
    """

    objects = UpdateSignalManager()

    class Meta:
        abstract = True
