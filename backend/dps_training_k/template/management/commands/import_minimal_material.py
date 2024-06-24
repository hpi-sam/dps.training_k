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
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Blutwärmer",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            name="Erythrozytenkonzentrat",
            category=Material.Category.BLOOD,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTBANK,
            name="Blutbank",  # Not really a device but more of a location in a hospital
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_1,
            name="Gerät 1",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.COMPUTERTOMOGRAPHIE,
            name="Computertomographie",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        # needed for patient_instance#get_fulfilled_subconditions
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
            name="Tragbares Beatmungsgerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_STATIONAER,
            name="Stationäres Beatmungsgerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
        )
