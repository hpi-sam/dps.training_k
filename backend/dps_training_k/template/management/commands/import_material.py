from django.core.management.base import BaseCommand

from template.constants import MaterialIDs
from template.models import Material


class Command(BaseCommand):
    help = "Populates the database with material list"

    def handle(self, *args, **kwargs):
        self.create_resources()
        self.stdout.write(
            self.style.SUCCESS("Successfully added material list to the database")
        )

    @staticmethod
    def create_resources():
        Material.objects.update_or_create(
            uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            name="Erythrozytenkonzentrat",
            category=Material.Category.BLOOD,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.FRESH_FROZEN_PLASMA,
            name="Fresh Frozen Plasma",
            category=Material.Category.BLOOD,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LYOPHILISIERTES_FRISCHPLASMA,
            name="Lyophilisiertes Frischplasma",
            category=Material.Category.BLOOD,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            name="Blutwärmer",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
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
            uuid=MaterialIDs.LAB_GERAET_2,
            name="Gerät 2",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_3,
            name="Gerät 3",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SONOGRAPHIE,
            name="Sonographie",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.EKG,
            name="EKG-Gerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.COMPUTERTOMOGRAPHIE,
            name="Computertomographie",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
            is_lab=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ROENTGENGERAET,
            name="Röntgengerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,  # in reality there also exist mobile devices
            is_lab=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ZVD_MESSGERAET,
            name="ZVD-Messgerät",  # ZVD = Zentraler Venendruck
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BZ_MESSGERAET,
            name="BZ-Messgerät",  # BZ = Blutzucker
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
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
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_TRAGBAR,
            name="Tragbarer Sauerstoff",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_STATIONAER,
            name="Stationärer Sauerstoff",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.DEFI_TRANSKUTANER_PACER,
            name="Defi + transkutaner Pacer",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PASSAGERER_PACER,
            name="Passagerer Pacer",
            category=Material.Category.DEVICE,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PERFUSORPUMPE,
            name="Perfusorpumpe",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.NARKOSEGERAET,
            name="Narkosegerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=False,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTGASANALYSE,
            name="Blutgasanalysegerät",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,  # in reality there also exist stationary devices
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
            uuid=MaterialIDs.BEATMUNGSBEUTEL,
            name="Beatmungsbeutel",
            category=Material.Category.DEVICE,
            is_reusable=False,
            is_moveable=True,
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SPRITZENPUMPE,
            name="Spritzenpumpe",
            category=Material.Category.DEVICE,
            is_reusable=True,
            is_moveable=True,
        )
