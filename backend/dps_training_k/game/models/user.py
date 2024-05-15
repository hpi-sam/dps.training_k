from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.db.models.signals import post_save, pre_delete
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from .patient_instance import PatientInstance


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    class UserType(TextChoices):
        PATIENT = "P", "Patient"
        TRAINER = "T", "Trainer"

    user_type = models.CharField(
        choices=UserType.choices, default=UserType.PATIENT, max_length=1
    )
    channel_name = models.CharField(max_length=100, null=True, blank=True)

    def is_player(self):
        return self.user_type == self.UserType.PATIENT

    def is_trainer(self):
        return self.user_type == self.UserType.TRAINER

    def set_channel_name(self, channel_name):
        self.channel_name = channel_name
        self.save()

    def clear_channel_name(self):
        self.channel_name = None
        self.save()


# create a token for the user upon sign up
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_delete, sender=PatientInstance)
def delete_patient(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
