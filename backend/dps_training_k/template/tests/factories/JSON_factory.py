from faker import Faker
import json


class JSONFactory:
    """Takes a dict and fills empty values with random values each time generate() is called."""

    def __new__(cls, dict):
        """Needed to copy interface of factory"""
        instance = super().__new__(cls)
        instance.__init__(dict)
        return instance.generate()

    def __init__(self, dict):
        self.random = Faker()
        self.dict = dict

    def generate(self):
        r_dict = self.dict
        for key, value in r_dict.items():
            if not value:
                r_dict[key] = self.random.sentence()
        return json.dumps(r_dict)
