from django.core.management.base import BaseCommand

from data.materials_data import update_or_create_materials


class Command(BaseCommand):
    help = "Populates the database with material list"

    def handle(self, *args, **kwargs):
        update_or_create_materials()
        self.stdout.write(
            self.style.SUCCESS("Successfully added material list to the database")
        )
