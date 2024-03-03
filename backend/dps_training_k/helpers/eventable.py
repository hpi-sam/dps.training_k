"""from django.db.models.base import ModelBase
from abc import ABCMeta, abstractmethod


# Create a new metaclass that inherits from both ModelBase and ABCMeta
class CustomModelBase(ABCMeta, ModelBase):
    pass
"""

from abc import abstractmethod


class AbstractEventable:

    @abstractmethod
    def schedule_events(self):
        pass

    @abstractmethod
    def remove_events(self):
        pass


class NonEventable(AbstractEventable):

    def schedule_events(self):
        pass

    def remove_events(self):
        pass


class Eventable(AbstractEventable):
    class Meta:
        abstract = True

    def remove_events(self):
        for event in self.owned_events.all():
            event.delete()


"""


class AbstractEventable:

    @abstractmethod
    def schedule_events(self):
        pass

    @abstractmethod
    def remove_events(self):
        pass


class NonEventable(AbstractEventable):

    def schedule_events(self):
        pass

    def remove_events(self):
        pass


class Eventable(AbstractEventable):
    class Meta:
        abstract = True

    def remove_events(self):
        for event in self.owned_events.all():
            event.delete()
"""
