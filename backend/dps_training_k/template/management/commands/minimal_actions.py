import json

from django.core.management.base import BaseCommand

from template.constants import (
    ActionIDs,
    MaterialIDs,
    RoleIDs,
    role_map,
)
from template.models import Action


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        self.create_actions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added minimal actions to the database")
        )

    @staticmethod
    def create_actions():
        # Treatments
        Action.objects.update_or_create(
            name="i.V. Zugang",
            uuid=ActionIDs.IV_ZUGANG,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "application_duration": 60,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt",
            uuid=ActionIDs.VOLLELEKTROLYT,
            defaults={
                "category": "TR",
                "application_duration": 5,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    }
                ),
                "results": json.dumps({}),
            },
        )
        # Examinations
        Action.objects.update_or_create(
            name="Hämoglobinanalyse",
            uuid=ActionIDs.HAEMOGLOBINANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "application_duration": 10,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            [
                                {role_map[RoleIDs.ARZT]: 1},
                                {role_map[RoleIDs.LABORASSISTENT]: 1},
                            ],
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Hb": {
                            400: 9.5,
                            401: 12,
                            402: 16,
                            403: 11,
                            404: 5.5,
                            405: 13,
                            406: 7.5,
                            407: 6,
                            408: 9,
                            409: 3.5,
                            410: 3,
                            411: 13,
                            412: 17,
                            413: 8,
                            414: 2.5,
                            415: 8.5,
                            416: 17,
                            417: 6.5,
                            418: 12,
                            419: 7,
                            420: 11,
                            421: 14,
                            422: 10,
                            423: 15,
                            424: 16,
                            425: 4,
                            426: 2,
                            427: 15,
                            428: 5,
                            429: 4.5,
                            430: 14,
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutgruppe bestimmen",
            uuid=ActionIDs.BLUTGRUPPE_BESTIMMEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "application_duration": 10,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Blutgruppe": {
                            1: "A Rh pos",
                            2: "B Rh pos",
                            3: "A rh neg",
                            4: "0 Rh pos",
                            5: "B rh neg",
                            6: "AB rh neg",
                            7: "O rh neg",
                            8: "AB Rh pos",
                        }
                    }
                ),
            },
        )
        # Relocating
        Action.objects.update_or_create(
            name="Trauma CT",
            uuid=ActionIDs.TRAUMA_CT,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": True,
                "application_duration": 10,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 3,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.MTRA]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Trauma-CT": {
                            100: "deutlich vergrößertes Herz, Aorta elongiert, Belüftung oB. Extremitäten: Normalbefund; keine Frakturzeichen;",
                            105: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales vermutlich gekapseltes Hämatom abdominal ca 2 L",
                            106: "Thorax: Normalbefund; Spiralfraktur rechter Oberarm; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            108: "leichte Stauungszeichen hilär komplette Unterarmfraktur re.",
                            112: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 3 cm; wenig Blut im unteren Resessus re.; beginnendes Hautemphysem re. lateral; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            121: "Thorax: Normalbefund; komplette Unterarmfraktur li. mit dezenter Verschiebung. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            123: "inhomogene Verschattungen, bds zentrale Infiltrate. Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales gekapseltes Hämatom abdominal mind 2 L",
                            130: "seitengleiche Belüftung; keine Ergüsse; kein Pneu; nicht dislozierte, sternumnahe Fraktur 4.Rippe li.; Oberarmamputation li.; sonst keine Frakturzeichen oder Fremdkörper; HWS: oB.; Becken: oB.;",
                            135: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 1,5 cm; wenig Blut im unteren Resessus re.; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            136: "inhomogene Verschattungen, bds zentrale Infiltrate Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; kleines zentrales Hämatom abdominal ca. 300 ml",
                            137: "Rippenserienfraktur re. 4-7; kompletter Pneumothorax re. mit Verlagerung des gesamten Mediastinums; ausgedehntes Hautemphysem; Lunge nur links ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            148: "Lunge noch deutlich überwässert; Pleuraergüsse bds. Extremitäten: Normalbefund; keine Frakturzeichen;",
                            152: "sgl Belüftung; beginnende Infiltrate bds. Basal, kleine Ergüsse Extremitäten: Normalbefund; keine Frakturzeichen; mind. 1 L Aszites; Pankreas aufgelockert, mehrere Pseudozysten",
                            159: "Thorax: Normalbefund; Oberschenkelfraktur re; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            161: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung; Metallcerclage wie nach Sternotomie;",
                            162: "Thorax: deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; keine Frakturen, gleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            173: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 2 l Blut im Abdomen; Leber fraglich rupturiert.",
                            174: "Thorax: großes Herz, geringgradige Stauung der Lunge, Belüftung seitengleich HüftTEP; sonst keine Auffälligkeiten",
                            175: "sgl Belüftung; beginnende Infiltrate bds. Basal Extremitäten: Normalbefund; keine Frakturzeichen;",
                            176: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; dezente Mittelllinienverschiebung; beginnendes Hirnödem linkshemisphärisch;",
                            185: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales ausgedehntes Hämatom abdominal mind 2 - 2,5 L",
                            189: "Rippenserienfraktur re. 4-7; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            191: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 3 l Blut im Abdomen; Leber fraglich rupturiert.",
                            196: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; Dünndarmschlingen aufgetrieben, Darmwand im Ileumbereich deutlich verdickt, ca. 200 ml freie Flüssigkeit",
                            205: "Thorax: Normalbefund; Dislozierte Handgelenksfraktur; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            207: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1 l Blut im Abdomen; Leber fraglich rupturiert.",
                            209: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung Oberschenkeltrummerfraktur re.",
                            221: "Sternumfraktur im mittleren Drittel Sprunggelenksfraktur mit deutlicher Dislokation",
                            228: "Thorax: Normalbefund; nicht dislozierte Sprunggelengsfraktur; sonst Extr. OB. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: Nasenbeinfraktu; fragliche Orbitabodenfraktur re.; fragliche Fissur Occipital; keine ICB, keine Raumforderung;",
                            236: "linke Lunge deutlich überbläht, Mediastinum dezent nach links verschoben; mehrere große Bullae; basal bds Infiltrate, Herz grenzwertig groß wie bei Rechtsbelastung Extremitäten: Normalbefund; keine Frakturzeichen;",
                            237: "Thorax: seitengleiche Belüftung; keine Ergüsse; kein Pneu; Rippenserienfraktur rechts lateral 3-6; Extremitäten: Oberschenkelfraktur bds. im mittleren Drittel;",
                            238: "Pleuraergüsse bds, Lunge inhomogen verschattet, Belüftung seitengleich, Thoraxskelet oB; Extremitäten: Normalbefund; keine Frakturzeichen;",
                            242: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            243: "Schrittmacheraggregat links subclavikulär, Kabel an loco tipico, Lunge dezent parahilär gestaut, keine Ergüsse; Extremitäten: Normalbefund; keine Frakturzeichen;",
                            248: "Rippenserienfraktur re. 3-7 ohne Pneu Trümmerfraktur des distalen US re.; komplette proximale Unterarmfraktur re.",
                            260: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; mehrere Fremdkörper in beiden Händen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            269: "Pneumothorax re. ca. 2 cm Oberschenkelschaftfraktur li mit Fehlstellung",
                            273: "Thorax: Lobärpneumonie links; deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; seitengleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; Pneumonische Infiltrate links und beginnend rechts, kleiner Pleuraerguss re.",
                            274: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1,5 l Blut im Abdomen; Leber fraglich rupturiert.",
                            281: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; keine Mittelllinienverschiebung; kein Hirnödem;",
                        }
                    }
                ),
            },
        )

        Action.objects.update_or_create(
            name="Operation einleiten",
            uuid=ActionIDs.OP_EINLEITEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.LAB,
                "relocates": True,
                "application_duration": 360000,  # 100h to assure that the operation never finishes during an exercise
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,  # garbage values
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        # Produce Material
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma (0 positiv) auftauen",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_AUFTAUEN,
            defaults={
                "category": Action.Category.PRODUCTION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 20,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "produced_material": {
                            str(MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS): 1
                        }
                    }
                ),
            },
        )
