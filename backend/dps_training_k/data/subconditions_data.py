from template.constants import ActionIDs, MaterialIDs
from template.models import Subcondition

CUSTOM_MAXINT = 100000  # doesn't matter, people shouldn't be doing the same thing 100000 times anyway


def update_or_create_subconditions():
    """
    name="Lyse", // name of subcondition
    upper_limit=CUSTOM_MAXINT, // maximum number of occurrences of fulfilling actions or fulfilling materials
    lower_limit=1, // minimum number of occurrences of fulfilling actions or fulfilling materials
    fulfilling_measures={
        "actions": {str(ActionIDs.LYSE_VERARBREICHEN): 1},
        "materials": {},
    }, // actions / materials that fulfill this subcondition. everything is or-connected. and-connection is not possible with current implementation
    """

    # corresponds to "Lyse"
    Subcondition.objects.update_or_create(
        name="Lyse",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.LYSE_VERARBREICHEN): 1},
            "materials": {},
        },
    )
    # corresponds to "4 EK´s"
    Subcondition.objects.update_or_create(
        name="4 EK´s",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=4,
        fulfilling_measures={
            "actions": {str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN): 1},
            "materials": {},
        },
    )
    # corresponds to "Infusion"
    Subcondition.objects.update_or_create(
        name="0-1l Infusion",
        upper_limit=999,
        lower_limit=0,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.VOLLELEKTROLYT_1000): 1000,
                str(ActionIDs.VOLLELEKTROLYT_500): 500,
            },
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="1-2l Infusion",
        upper_limit=1999,
        lower_limit=1000,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.VOLLELEKTROLYT_1000): 1000,
                str(ActionIDs.VOLLELEKTROLYT_500): 500,
            },
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="2-3l Infusion",
        upper_limit=2999,
        lower_limit=2000,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.VOLLELEKTROLYT_1000): 1000,
                str(ActionIDs.VOLLELEKTROLYT_500): 500,
            },
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="3l-inf Infusion",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=3000,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.VOLLELEKTROLYT_1000): 1000,
                str(ActionIDs.VOLLELEKTROLYT_500): 500,
            },
            "materials": {},
        },
    )
    # corresponds to "2l Infusion"
    Subcondition.objects.update_or_create(
        name="2l Infusion",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=2000,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.VOLLELEKTROLYT_1000): 1000,
                str(ActionIDs.VOLLELEKTROLYT_500): 500,
            },
            "materials": {},
        },
    )
    # corresponds to "Thoraxdrainage/ Pleurapunktion"
    Subcondition.objects.update_or_create(
        name="Thoraxdrainage/ Pleurapunktion",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.THORAXDRAINAGE): 1,
                str(ActionIDs.PLEURAPUNKTION): 1,
            },
            "materials": {},
        },
    )
    # corresponds to "Glucose"
    Subcondition.objects.update_or_create(
        name="Glucose",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.GLUCOSE_VERABREICHEN): 1},
            "materials": {},
        },
    )
    # corresponds to "Nitrat"
    Subcondition.objects.update_or_create(
        name="Nitrat",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.NITRAT): 1},
            "materials": {},
        },
    )
    # corresponds to O2
    Subcondition.objects.update_or_create(
        name="O2",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.SAUERSTOFF_ANBRINGEN): 1,
                str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN): 1,
            },
            "materials": {},
        },
    )
    # corresponds to "OP läuft / ist gelaufen" as well as "keine OP"
    Subcondition.objects.update_or_create(
        name="OP läuft / ist gelaufen",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={"actions": {}, "materials": {}},
    )
    # corresponds to "Analgesie"
    Subcondition.objects.update_or_create(
        name="Analgesie",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.ANALGETIKUM): 1},
            "materials": {},
        },
    )
    # corresponds to "O2 Inhalation"
    Subcondition.objects.update_or_create(
        name="O2 Inhalation",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.SAUERSTOFF_ANBRINGEN): 1,
                str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN): 1,
            },
            "materials": {},
        },
    )
    # corresponds to "CPAP"
    Subcondition.objects.update_or_create(
        name="CPAP",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.CPAP_BEATMUNGSGERAET_ANBRINGEN): 1},
            "materials": {},
        },
    )
    # corresponds to "Antiasthmatikum"
    Subcondition.objects.update_or_create(
        name="Antiasthmatikum",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.ANTIASTHMATIKUM): 1},
            "materials": {},
        },
    )
    # corresponds to "Sedativum"
    Subcondition.objects.update_or_create(
        name="Sedativum",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.SEDATIVUM): 1},
            "materials": {},
        },
    )
    # corresponds to "freie Atemwege"
    Subcondition.objects.update_or_create(
        name="freie Atemwege",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.STABILE_SEITENLAGE): 1,
                str(ActionIDs.GUEDELTUBUS): 1,
                str(ActionIDs.WENDELTUBUS): 1,
                str(ActionIDs.TRACHEALTUBUS): 1,
                str(ActionIDs.LARYNXMASKE): 1,
                str(ActionIDs.LARYNXTUBUS): 1,
            },
            "materials": {},
        },
    )
    # corresponds to "EK´s"
    Subcondition.objects.update_or_create(
        name="0-1 EK´s",
        upper_limit=1,
        lower_limit=0,
        fulfilling_measures={
            "actions": {str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN): 1},
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="2-3 EK´s",
        upper_limit=3,
        lower_limit=2,
        fulfilling_measures={
            "actions": {str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN): 1},
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="4-5 EK´s",
        upper_limit=5,
        lower_limit=4,
        fulfilling_measures={
            "actions": {str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN): 1},
            "materials": {},
        },
    )
    Subcondition.objects.update_or_create(
        name="6-inf EK´s",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=6,
        fulfilling_measures={
            "actions": {str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN): 1},
            "materials": {},
        },
    )
    # corresponds to "Beatmet"
    Subcondition.objects.update_or_create(
        name="Beatmet",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN): 1},
            "materials": {
                str(MaterialIDs.BEATMUNGSGERAET_STATIONAER): 1,
                str(MaterialIDs.BEATMUNGSGERAET_TRAGBAR): 1,
            },
        },
    )
    # corresponds to Blutstillung
    Subcondition.objects.update_or_create(
        name="Blutstillung",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {str(ActionIDs.CHIR_BLUTSTILLUNG): 1},
            "materials": {},
        },
    )
    # corresponds to "Regional-/ Vollnarkose"
    Subcondition.objects.update_or_create(
        name="Regional-/ Vollnarkose",
        upper_limit=CUSTOM_MAXINT,
        lower_limit=1,
        fulfilling_measures={
            "actions": {
                str(ActionIDs.REGIONAL_NARKOSE): 1,
                str(ActionIDs.REGIONAL_NARKOTIKUM): 1,
                str(ActionIDs.NARKOTIKUM): 1,
            },
            "materials": {},
        },
    )
