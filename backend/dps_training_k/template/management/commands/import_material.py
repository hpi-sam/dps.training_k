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
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTAUFTAU_SLOT,
            name="Blutauftau-Slot",
            category=Material.Category.LABOR,
            is_reusable=True,
            used=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Wärmegerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            used=True,
        )

        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_1,
            name="Gerät 1",
            category=Material.Category.LABOR,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SONOGRAPHIE,
            name="Sonographie",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.EKG,
            name="EKG-Gerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.COMPUTERTOMOGRAPHIE,
            name="Computertomographie",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ZVD_MESSGERAET,
            name="ZVD-Messgerät",  # ZVD = Zentraler Venendruck
            category=Material.Category.DEVICE,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BZ_MESSGERAET,
            name="BZ-Messgerät",  # BZ = Blutzucker
            category=Material.Category.DEVICE,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.MONITOR_TRAGBAR,
            name="Tragbarer Monitor",
            category=Material.Category.DEVICE,
            is_reusable=True,
            moveable=True,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.MONITOR_STATIONAER,
            name="Stationärer Monitor",
            category=Material.Category.DEVICE,
            is_reusable=True,
            moveable=False,
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
            uuid=MaterialIDs.BEATMUNGSGERAET_STATIONAER,
            name="Stationäres Beatmungsgerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            moveable=False,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_TRAGBAR,
            name="Tragbarer Sauerstoff",
            category=Material.Category.DEVICE,
            moveable=True,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_STATIONAER,
            name="Stationärer Sauerstoff",
            category=Material.Category.DEVICE,
            moveable=False,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.DEFI_TRANSCUTANER_PACER,
            name="Defi + transcutaner Pacer",
            category=Material.Category.DEVICE,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PASSAGERER_PACER,
            name="Passagerer Pacer",
            category=Material.Category.DEVICE,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PERFUSORPUMPE,
            name="Perfusorpumpe",
            category=Material.Category.DEVICE,
            used=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.NARKOSEGERAET,
            name="Narkosegerät",
            category=Material.Category.DEVICE,
            used=True,
        )
