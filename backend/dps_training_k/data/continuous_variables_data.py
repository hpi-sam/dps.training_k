from template.constants import ActionIDs, MaterialIDs, ContinuousVariableIDs
from template.models.continuous_variable import ContinuousVariable


def update_or_create_continuous_variables():
    """
    "name": ContinuousVariable.Variable.SPO2, // name as defined in ContinuousVariable
    "function": ContinuousVariable.Function.LINEAR, // function as defined in ContinuousVariable
    "exceptions": [{
        "actions": ["A1uuid", ["A2uuid", "A3uuid"]], // this means action1 OR (action3 AND action4); can be None
        "materials": ["M1uuid", ["M2uuid", "M3uuid"]], // material1 OR material2 OR (material3 AND material4); can be None
        "function": ContinuousVariable.Function.LINEAR, // function as defined in ContinuousVariable
    }] // exceptions listed according to their priority. If the first exceptions applies, the rest won't be looked at
    // actions and materials both need to be true in order for the exception to apply
    """

    ContinuousVariable.objects.update_or_create(
        uuid=ContinuousVariableIDs.SPO2,
        defaults={
            "name": ContinuousVariable.Variable.SPO2,
            "function": ContinuousVariable.Function.LINEAR,
            "exceptions": [
                {
                    "actions": [str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN)],
                    "materials": [
                        str(MaterialIDs.BEATMUNGSGERAET_STATIONAER),
                        str(MaterialIDs.BEATMUNGSGERAET_TRAGBAR),
                    ],
                    "function": ContinuousVariable.Function.LINEAR,
                },
                {
                    "actions": [
                        [str(ActionIDs.IV_ZUGANG), str(ActionIDs.DRUCKVERBAND)]
                    ],
                    "materials": [
                        [str(MaterialIDs.EKG), str(MaterialIDs.BZ_MESSGERAET)]
                    ],
                    "function": ContinuousVariable.Function.DECREMENT,
                },
                {
                    "actions": [str(ActionIDs.IV_ZUGANG)],
                    "materials": [str(MaterialIDs.EKG)],
                    "function": ContinuousVariable.Function.INCREMENT,
                },
                {
                    "actions": [str(ActionIDs.IV_ZUGANG)],
                    "materials": [],
                    "function": ContinuousVariable.Function.SIGMOID,
                },
            ],
        },
    )
    ContinuousVariable.objects.update_or_create(
        uuid=ContinuousVariableIDs.HEART_RATE,
        defaults={
            "name": ContinuousVariable.Variable.HEART_RATE,
            "function": ContinuousVariable.Function.LINEAR,
            "exceptions": [],
        },
    )
