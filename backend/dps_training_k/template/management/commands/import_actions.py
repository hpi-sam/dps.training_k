from django.core.management.base import BaseCommand

from data.actions_data import update_or_create_actions


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        update_or_create_actions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added actions to the database")
        )
