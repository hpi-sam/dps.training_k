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
            defaults={
                "name": "Erythrozytenkonzentrat",
                "category": Material.Category.BLOOD,
                "is_reusable": False,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.FRESH_FROZEN_PLASMA,
            defaults={
                "name": "Fresh Frozen Plasma",
                "category": Material.Category.BLOOD,
                "is_reusable": False,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LYOPHILISIERTES_FRISCHPLASMA,
            defaults={
                "name": "Lyophilisiertes Frischplasma",
                "category": Material.Category.BLOOD,
                "is_reusable": False,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE,
            defaults={
                "name": "Blutwärmer",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_1,
            defaults={
                "name": "Gerät 1",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_2,
            defaults={
                "name": "Gerät 2",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.LAB_GERAET_3,
            defaults={
                "name": "Gerät 3",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SONOGRAPHIE,
            defaults={
                "name": "Sonographie",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.EKG,
            defaults={
                "name": "EKG-Gerät",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.COMPUTERTOMOGRAPHIE,
            defaults={
                "name": "Computertomographie",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ROENTGENGERAET,
            defaults={
                "name": "Röntgengerät",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },  # in reality there also exist mobile devices
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ZVD_MESSGERAET,
            defaults={
                "name": "ZVD-Messgerät",  # ZVD = Zentraler Venendruck
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BZ_MESSGERAET,
            defaults={
                "name": "BZ-Messgerät",  # BZ = Blutzucker
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
            defaults={
                "name": "Beatmungsgerät (Tragbar)",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_STATIONAER,
            defaults={
                "name": "Beatmungsgerät (Stationäres)",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSGERAET_CPAP,
            defaults={
                "name": "Beatmungsgerät (CPAP)",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_TRAGBAR,
            defaults={
                "name": "Sauerstoff (Tragbarer)",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SAUERSTOFF_STATIONAER,
            defaults={
                "name": "Sauerstoff (Stationärer)",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.DEFI_TRANSKUTANER_PACER,
            defaults={
                "name": "Defi + transkutaner Pacer",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PASSAGERER_PACER,
            defaults={
                "name": "Passagerer Pacer",
                "category": Material.Category.DEVICE,
                "is_reusable": False,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.PERFUSORPUMPE,
            defaults={
                "name": "Perfusorpumpe",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.NARKOSEGERAET,
            defaults={
                "name": "Narkosegerät",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTGASANALYSE,
            defaults={
                "name": "Blutgasanalysegerät",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },  # in reality there also exist stationary devices
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BLUTBANK,
            defaults={
                "name": "Blutbank",  # Not really a device but more of a location in a hospital
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": False,
                "is_lab": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.BEATMUNGSBEUTEL,
            defaults={
                "name": "Beatmungsbeutel",
                "category": Material.Category.DEVICE,
                "is_reusable": False,
                "is_moveable": True,
            },
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.SPRITZENPUMPE,
            defaults={
                "name": "Spritzenpumpe",
                "category": Material.Category.DEVICE,
                "is_reusable": True,
                "is_moveable": True,
            },
        )
