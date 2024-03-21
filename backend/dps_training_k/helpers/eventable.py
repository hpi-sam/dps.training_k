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

    def remove_events(self):
        for event in self.owned_events.all():
            event.delete()
