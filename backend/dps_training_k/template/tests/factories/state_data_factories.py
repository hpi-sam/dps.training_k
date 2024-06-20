from faker import Faker


class VitalSignsData:
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
        instance = super().__new__(cls)
        instance.__init__(state_data_dict)
        return instance.generate()

    def __init__(self, dict):
        self.random = Faker()
        self.dict = dict

    def generate(self):
        r_dict = self.dict
        for key, value in r_dict.items():
            if not value:
                r_dict[key] = self.random.sentence()
        return r_dict


class ExaminationCodesData:
    def __new__(cls):
        instance = super().__new__(cls)
        return instance.generate()

    @staticmethod
    def generate(
        bga_oxy="600",
        bga_sbh="650",
        ekg="701",
        bz="901",
        zvd="800",
        ro_extremitaeten="511",
        ro_thorax="305",
        ct="100",
        ultraschall="502",
        blutgruppe="1",
        hb="400",
        lactat="140",
        gerinnung="100",
        leber="110",
        niere="120",
        infarkt="130",
    ):
        return {
            "BGA-Oxy": bga_oxy,
            "BGA-SBH": bga_sbh,
            "EKG": ekg,
            "BZ": bz,
            "ZVD": zvd,
            "Rö-Extremitäten": ro_extremitaeten,
            "Rö-Thorax": ro_thorax,
            "CT": ct,
            "Ultraschall": ultraschall,
            "Blutgruppe": blutgruppe,
            "Hb": hb,
            "Lactat": lactat,
            "Gerinnung": gerinnung,
            "Leber": leber,
            "Niere": niere,
            "Infarkt": infarkt,
        }
