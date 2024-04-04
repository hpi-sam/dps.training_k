from .JSON_factory import JSONFactory


class StateDataFactory(JSONFactory):
    def __init__(self):
        state_data_dict = {
            "airway": None,
            "breathing": None,
            "circulation": None,
            "consciousness": None,
            "pupils": None,
            "psyche": None,
            "skin": None,
        }
        super().__init__(state_data_dict)
