from abc import abstractmethod


class AbstractEventable:
    class Meta:
        abstract = True

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
