from datetime import datetime
from abc import abstractmethod


class NameGenerator:
    @abstractmethod
    def generate_name(self):
        pass


class DateTimeNameGenerator(NameGenerator):
    def __init__(
        self,
    ):
        self.last_base_name = ""
        self.same_name_count = 1

    def generate_name(self):
        name = datetime.now().strftime("%d.%m.%y %H:%M:%S")
        if name == self.last_base_name:
            self.last_base_name = name
            name = name + "(" + str(self.same_name_count) + ")"
            self.same_name_count += 1
        else:
            self.last_base_name = name
            self.same_name_count = 1
        return name
