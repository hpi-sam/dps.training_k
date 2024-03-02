from django.db import models
from abc import abstractmethod


class Eventable(models.Model):
    class Meta:
        abstract = True

    @abstractmethod
    def schedule_events(self):
        pass

    def remove_events(self):
        for event in self.owned_events.all():
            event.delete()


class NestedEventable(Eventable):
    def schedule_events_globally(self):
        self.schedule_events()
        nested_eventables = self.nested_eventables()
        for eventable in nested_eventables:
            eventable.schedule_events_globally()

    def remove_events_globally(self):
        self.remove_events()
        nested_eventables = self.nested_eventables()
        for eventable in nested_eventables:
            eventable.remove_events_globally()

    @abstractmethod
    def nested_eventables(self):
        pass
