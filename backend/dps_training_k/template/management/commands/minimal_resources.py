from django.core.management.base import BaseCommand
from template.models import Resource
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
        Resource.objects.update_or_create(
            name="Enthrozytenkonzentrat 0 pos.",
            is_returnable=False,
            uuid=MaterialIDs.CONCENTRATED_RED_CELLS_0_POS,
        )
