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
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
            name="Tragbares Beatmungsgerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            moveable=True,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Wärmegerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            used=True,
        )
