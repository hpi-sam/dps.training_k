from django.core.management.base import BaseCommand
from template.models import Action

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        Action.objects.update_or_create(name="stabile Seitenlage", category="TR", duration=10, conditions={"test":"test"})
        self.stdout.write(self.style.SUCCESS('Successfully added data to the database'))
        all_objects = Action.objects.all()
        for obj in all_objects:
            self.stdout.write(obj.name)