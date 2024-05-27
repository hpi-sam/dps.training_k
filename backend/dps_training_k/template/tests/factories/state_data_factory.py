from .JSON_factory import JSONFactory
from template.constants import ActionResultIDs


class VitalSignsData(JSONFactory):
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


class ExaminationCodesData(JSONFactory):
    def __new__(cls):
        """Needed to copy interface of factory"""

        state_data_dict = {
            "BGA-Oxy": 600,
            "BGA-SBH": 650,
            "EKG": 701,
            "BZ": 900,
            "ZVD": 800,
            "Rö-Extremitäten": 511,
            "Rö-Thorax": 305,
            "CT": 100,
            "Ultraschall": 502,
            "Blutgruppe": 1,
            "Hb": 400,
            "Lactat": 140,
            "Gerinnung": 100,
            "Leber": 110,
            "Niere": 120,
            "Infarkt": 130,
        }
        return super().__new__(cls, state_data_dict)
