from .JSON_factory import JSONFactory


class StateDataFactory(JSONFactory):
    def __new__(cls):
        """Needed to copy interface of factory"""

        state_data_dict = {
            "airway": None,
            "breathing": None,
            "circulation": None,
            "consciousness": None,
            "pupils": None,
            "psyche": None,
            "skin": None,
        }
        return super().__new__(cls, state_data_dict)
