from django.core.management.base import BaseCommand
from template.models import Material
from template.constants import MaterialIDs


class Command(BaseCommand):
    help = "Populates the database with minimal resources list"

    def handle(self, *args, **kwargs):
        self.create_resources()
        self.stdout.write(
            self.style.SUCCESS("Successfully added resources to the database")
        )

    @staticmethod
    def create_resources():
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTAUFTAU_SLOT,
            name="Blutauftau-Slot",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET,
            name="Beatmungsgerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Wärmegerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
