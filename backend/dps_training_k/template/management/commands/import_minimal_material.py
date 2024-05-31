from django.core.management.base import BaseCommand

from template.constants import MaterialIDs
from template.models import Material


class Command(BaseCommand):
    help = "Populates the database with minimal material list"

    def handle(self, *args, **kwargs):
        self.create_resources()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully added minimal material list to the database"
            )
        )

    @staticmethod
    def create_resources():
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT,
            name="Enthrozytenkonzentrat",
            category=Material.Category.BLOOD,
            reusable=False,
            moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Blutwärmer",
            category=Material.Category.LABOR,
            reusable=True,
            moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_1,
            name="Gerät 1",
            category=Material.Category.LABOR,
            reusable=True,
            moveable=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSBEUTEL,
            name="Beatmungsbeutel",
            category=Material.Category.DEVICE,
            reusable=False,
            moveable=True,
        )
