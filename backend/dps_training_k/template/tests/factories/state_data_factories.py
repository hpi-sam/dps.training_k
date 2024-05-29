from .JSON_factory import JSONFactory


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
