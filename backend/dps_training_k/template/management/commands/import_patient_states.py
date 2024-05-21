from django.core.management.base import BaseCommand
import csv, json
from template.models import PatientState, Subcondition, LogicNode, StateTransition
from django.conf import settings
import os, re
from template.constants import ActionIDs
from time import sleep
from copy import deepcopy

CUSTOM_MAXINT = 100000  # doesn't matter, people shouldn't be doing the same thing 100000 times anyway


class Command(BaseCommand):
    help = "Populates the database with patient states."

    def handle(self, *args, **kwargs):
        self.create_subconditions()
        self.create_patient_states_and_transitions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added patient states to the database")
        )

    def create_subconditions(self):
        # corresponds to "Lyse"
        Subcondition.objects.update_or_create(
            name="keine Lyse",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.LYSE_VERARBREICHEN): 0},
        )
        Subcondition.objects.update_or_create(
            name="Lyse",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.LYSE_VERARBREICHEN): 1},
        )
        # corresponds to "4 EK´s"
        Subcondition.objects.update_or_create(
            name="0-3 EKs",
            upper_limit=3,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 0},
        )
        Subcondition.objects.update_or_create(
            name="4-inf EKs",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=4,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 4},
        )
        # corresponds to "Infusion"
        Subcondition.objects.update_or_create(
            name="0-999 Infusion",
            upper_limit=999,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="1000-1999 Infusion",
            upper_limit=1999,
            lower_limit=1000,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="2000-2999 Infusion",
            upper_limit=2999,
            lower_limit=2000,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="3000-inf Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=3000,
            fulfilling_measures={},
        )
        # corresponds to "2l Infusion"
        Subcondition.objects.update_or_create(
            name="0-1999 Infusion",
            upper_limit=1999,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="2000-inf Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=2000,
            fulfilling_measures={},
        )
        # corresponds to "Thoraxdrainage/ Pleurapunktion"
        Subcondition.objects.update_or_create(
            name="keine Thoraxdrainage/ Pleurapunktion",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={
                str(ActionIDs.THORAXDRAINAGE): 0,
                str(ActionIDs.PLEURAPUNKTION): 0,
            },
        )
        Subcondition.objects.update_or_create(
            name="Thoraxdrainage/ Pleurapunktion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                str(ActionIDs.THORAXDRAINAGE): 1,
                str(ActionIDs.PLEURAPUNKTION): 1,
            },
        )
        # corresponds to "Glucose"
        Subcondition.objects.update_or_create(
            name="keine Glucose",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.GLUCOSE_VERABREICHEN): 0},
        )
        Subcondition.objects.update_or_create(
            name="Glucose",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.GLUCOSE_VERABREICHEN): 1},
        )
        # corresponds to "Nitrat"
        Subcondition.objects.update_or_create(
            name="kein Nitrat",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.NITRAT): 0},
        )
        Subcondition.objects.update_or_create(
            name="Nitrat",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.NITRAT): 1},
        )
        # corresponds to O2
        Subcondition.objects.update_or_create(
            name="kein O2",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="O2",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "OP läuft / ist gelaufen" as well as "keine OP"
        Subcondition.objects.update_or_create(
            name="keine OP läuft / ist gelaufen",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="OP läuft / ist gelaufen",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "Analgesie"
        Subcondition.objects.update_or_create(
            name="keine Analgesie",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.ANALGETIKUM): 0},
        )
        Subcondition.objects.update_or_create(
            name="Analgesie",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.ANALGETIKUM): 1},
        )
        # corresponds to "O2 Inhalation"
        Subcondition.objects.update_or_create(
            name="keine O2 Inhalation",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="O2 Inhalation",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "CPAP"
        Subcondition.objects.update_or_create(
            name="kein CPAP",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="CPAP",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "Antiasthmatikum"
        Subcondition.objects.update_or_create(
            name="kein Antiasthmatikum",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.ANTIASTHMATIKUM): 0},
        )
        Subcondition.objects.update_or_create(
            name="Antiasthmatikum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.ANTIASTHMATIKUM): 1},
        )
        # corresponds to "Sedativum"
        Subcondition.objects.update_or_create(
            name="kein Sedativum",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.SEDATIVUM): 0},
        )
        Subcondition.objects.update_or_create(
            name="Sedativum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.SEDATIVUM): 1},
        )
        # corresponds to "freie Atemwege"
        Subcondition.objects.update_or_create(
            name="keine freien Atemwege",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="freie Atemwege",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "EK´s"
        Subcondition.objects.update_or_create(
            name="0-1 EKs",
            upper_limit=1,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 0},
        )
        Subcondition.objects.update_or_create(
            name="2-3 EKs",
            upper_limit=3,
            lower_limit=2,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 2},
        )
        Subcondition.objects.update_or_create(
            name="4-5 EKs",
            upper_limit=5,
            lower_limit=4,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 4},
        )
        Subcondition.objects.update_or_create(
            name="6-inf EKs",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=6,
            fulfilling_measures={str(ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN): 6},
        )
        # corresponds to "Beatmet"
        Subcondition.objects.update_or_create(
            name="Nicht beatmet",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.BEATMUNG): 0},
        )
        Subcondition.objects.update_or_create(
            name="Beatmet",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.BEATMUNG): 1},
        )
        # corresponds to Blutstillung
        Subcondition.objects.update_or_create(
            name="keine Blutstillung",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={str(ActionIDs.CHIR_BLUTSTILLUNG): 0},
        )
        Subcondition.objects.update_or_create(
            name="Blutstillung",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={str(ActionIDs.CHIR_BLUTSTILLUNG): 1},
        )
        # corresponds to "Regional-/ Vollnarkose"
        Subcondition.objects.update_or_create(
            name="keine Regional-/ Vollnarkose",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={
                str(ActionIDs.REGIONAL_NARKOSE): 1,
                str(ActionIDs.REGIONAL_NARKOTIKUM): 1,
                str(ActionIDs.NARKOTIKUM): 1,
            },
        )
        Subcondition.objects.update_or_create(
            name="Regional-/ Vollnarkose",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                str(ActionIDs.REGIONAL_NARKOSE): 1,
                str(ActionIDs.REGIONAL_NARKOTIKUM): 1,
                str(ActionIDs.NARKOTIKUM): 1,
            },
        )

    def create_patient_states_and_transitions(self):
        # outer loop to create all patients
        for i in range(1002, 1003):
            # parse data for specific patient
            self.patient_states = self.parse_patient_data(i)
            self.state_transitions = self.parse_state_transitions(i)
            # create first state, then go into recursion to create other states and all transitions
            first_patient_state = self.patient_states[0]
            self.patient_states = self.patient_states[1:]
            first_patient_state_obj = PatientState.objects.create(
                state_id=first_patient_state["state_id"],
                transition=None,
                data=first_patient_state["data"],
                is_dead=first_patient_state["is_dead"],
            )
            first_state_transition = self.create_state_transitions(
                first_patient_state["table_id"]
            )
            # finally, set the transition for the patient (first one of the linked list)
            first_patient_state_obj.transition = first_state_transition

    def create_patient_state(self, state_id):
        # find corresponding patient_state for state_id
        for patient_state in self.patient_states:
            if patient_state["state_id"] == int(state_id):
                break

        patient_state_obj, created = PatientState.objects.get_or_create(
            state_id=patient_state["state_id"],
            data=patient_state["data"],
            transition=None,
            is_dead=patient_state["is_dead"],
        )
        return patient_state_obj, created

    def create_state_transitions(self, table_id):
        sleep(0.05)
        # end of recursion
        if table_id == "":  # this is only the case if we're in a final state
            state_transition_obj = StateTransition.objects.create()
            LogicNode.objects.create(
                state_transition=state_transition_obj,
                node_type=LogicNode.NodeType.TRUE,
            )
            return state_transition_obj

        for i, table_id_data in enumerate(self.state_transitions["table_results"]):
            if table_id_data["table_id"] == table_id:
                break
        relevant_table_id_data = self.state_transitions["table_results"][i]

        # guard condition "Immer" forces next state without any conditions
        if "Immer:" in relevant_table_id_data["extra_condition 1"]:
            resulting_state_id = relevant_table_id_data["extra_condition 1"].split(
                "Immer: "
            )[1]
            resulting_patient_state_obj, created = self.create_patient_state(
                resulting_state_id
            )

            if created:
                print("was created")
                # get data for next transition
                for patient_state in self.patient_states:
                    if patient_state["state_id"] == int(resulting_state_id):
                        table_id = patient_state["table_id"]
                        break

                # recursive call to create transitions and resulting states for state created above
                resulting_state_transition = self.create_state_transitions(table_id)
                resulting_patient_state_obj.transition = resulting_state_transition
            else:
                print("caught existing state")

            # create transitions to resulting states
            # the "from original state" part needs to be set by caller
            first_state_transition = StateTransition.objects.create(
                resulting_state=resulting_patient_state_obj
            )
            LogicNode.objects.create(
                state_transition=first_state_transition, node_type=LogicNode.NodeType.TRUE
            )
        else:
            # create transitions for table 0
            table0 = self.state_transitions["table 0"]
            table0_subconditions = table0[0]
            # table0_subconditions.append(
            #     relevant_table_id_data["extra_condition 1"]
            # )  # TODO: handle case with multiple conditions here
            # TODO: fix this adding the same thing multiple times, maybe use set instead

            previous_state_transition = None
            first_state_transition = None
            for i, line in enumerate(table0[1:]):  # for each line of the table
                resulting_state_id = relevant_table_id_data["table_0_results"][i]
                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )

                if created:
                    print("was created")
                    # get data for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            break

                    # recursive call to create transitions and resulting states for state created above
                    resulting_state_transition = self.create_state_transitions(table_id)
                    resulting_patient_state_obj.transition = resulting_state_transition
                else:
                    print("caught existing state")

                # create transitions to resulting states
                # the "from original state" part needs to be set by caller
                state_transition = StateTransition.objects.create(
                    resulting_state=resulting_patient_state_obj
                )
                self.create_logic_nodes(
                    deepcopy(table0_subconditions),
                    deepcopy(relevant_table_id_data["extra_condition 1"]),
                )  # deepcopy enforces pass by value which is necessary to prevent adding extra conditions multiple times
                # save first transition for return value
                if not first_state_transition:
                    first_state_transition = state_transition
                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                previous_state_transition = state_transition

                # TODO: create logic nodes for each transition

            table1 = self.state_transitions["table 1"]
            # print(table1)
            table1_subconditions = table1[0]
            # table1_subconditions.append(relevant_table_id_data["extra_condition 2"])

            previous_state_transition = None
            first_state_transition = None
            # for i, line in enumerate(table1[1:]):  # basically for each line of the table
            for i in range(len(table1_subconditions)):
                # TODO: deal with second table being "leer"
                resulting_state_id = relevant_table_id_data["table_1_results"][i]
                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )
                # print(f"resulting state id: {resulting_state_id}, i: {i}, data: {relevant_table_id_data["table_0_results"]}, created: {created}")

                if created:
                    print("was created")
                    # get data for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            # print(f"table id: {table_id}")
                            break

                    # recursive call to create transitions and resulting states for state created above
                    resulting_state_transition = self.create_state_transitions(table_id)
                    resulting_patient_state_obj.transition = resulting_state_transition
                else:
                    print("caught existing state")

                # create transitions to resulting states
                # the "from original state" part needs to be set by caller
                state_transition = StateTransition.objects.create(
                    resulting_state=resulting_patient_state_obj
                )
                # save first transition for return value
                if not first_state_transition:
                    first_state_transition = state_transition
                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                previous_state_transition = state_transition

                # TODO: create logic nodes for each transition

        return first_state_transition

    def create_logic_nodes(self, table_subconditions, extra_conditions):
        # print(f"table subconditions: {table_subconditions}")
        # print(f"extra conditions: {extra_conditions}")
        if "Nicht beatmet" in extra_conditions:
            table_subconditions.append(Subcondition.objects.get(name="Nicht beatmet"))
        elif "Beatmet" in extra_conditions:
            table_subconditions.append(Subcondition.objects.get(name="Beatmet"))
        if "keine Lyse" in extra_conditions:
            pass

    def parse_state_transitions(self, patient_code):
        base_dir = os.path.join(settings.DATA_ROOT, "patient_states/")
        filename = str(patient_code) + "_tables.csv"
        full_path = os.path.join(base_dir, filename)
        state_transitions = {}
        with open(full_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            # TODO deal with empty tables
            table0 = []
            table1 = []
            table_results = []
            parsing_table_0 = False
            parsing_table_1 = False
            for row in reader:
                if row[0] == "Tabelle 0:":
                    parsing_table_0 = True
                elif row[0] == "Tabelle 1:":
                    parsing_table_1 = True
                    parsing_table_0 = False
                # parse both tables ("Tabelle 0" and "Tabelle 1") into matrix
                elif parsing_table_0:
                    table_data = row
                    table0.append(table_data)
                elif parsing_table_1:
                    table_data = row
                    table1.append(table_data)
                else:
                    print("something went wrong")

                # parse data of each table id
                if "Table-Id" in row[0]:
                    # creates 3 groups: table-id, extra conditions (e.g. Nicht Beatmet) and resulting states + potentially another condition
                    match = re.search(
                        r"Table-Id:\s+(\d+)\s+([a-zA-Z0-9\s:']+)(.*)", row[0]
                    )
                    if match:
                        table_id_data = {}  # data for one table id
                        table_id = match.group(1)
                        table_id_data["table_id"] = table_id
                        # TODO parse to subcondition instead of string
                        extra_conditions = match.group(2)
                        table_id_data["extra_condition 1"] = extra_conditions

                        # there are no resulting states if "Immer" is present
                        if "Immer" not in extra_conditions:
                            results = []
                            fields = match.group(3).split(", ")
                            for field in fields[1:]:  # ignore first cause its empty
                                field = field.replace("'", "")
                                results.append(field)

                            for index, resulting_state in enumerate(results):
                                if "Beatmet" in resulting_state:
                                    break

                            first_table_resulting_states = results[:index]
                            second_table_resulting_states = results[index + 1 :]
                            second_table_extra_condition = results[index]
                            table_id_data["extra_condition 2"] = (
                                second_table_extra_condition
                            )
                            table_id_data["table_0_results"] = (
                                first_table_resulting_states
                            )
                            table_id_data["table_1_results"] = (
                                second_table_resulting_states
                            )
                        else:
                            table_id_data["extra_condition 2"] = []
                            table_id_data["table_0_results"] = []
                            table_id_data["table_1_results"] = []

                    else:
                        print(f"couldn't find table-id for line {row[0]}")

                    table_results.append(table_id_data)

        table0[0] = [
            Subcondition.objects.get(name=subcondition) for subcondition in table0[0]
        ]

        state_transitions["table 0"] = table0
        state_transitions["table 1"] = table1
        state_transitions["table_results"] = table_results
        return state_transitions

    # builds all trees for one table_id
    def build_tree_for_table(self, table_id_data, table0, table1, patient_states):
        # guard condition invalidates table -> always same resulting state
        for patient_state in patient_states:
            patient_state_obj = PatientState.objects.create(
                state_id=patient_state["state_id"],
                transition=None,  # TODO: replace
                data=patient_state["data"],
                is_dead=patient_state["is_dead"],
            )

        if "Immer" in table_id_data[1]:
            resulting_state = table_id_data[1].split(" ")[1]
            new_state_transition = StateTransition.objects.create(
                next_state_transition=None,
            )  # TODO: add resulting_state. will need to store this state_transition together with its resulting_state (which isn't an object yet)
            LogicNode.objects.create(
                state_transition=new_state_transition,
                node_type=LogicNode.NodeType.TRUE,
            )
        elif (
            " 'Nicht beatmet'" in table_id_data[1]
        ):  # this should only match lines that don't have any other extra conditions
            # split resulting states into the two tables they belong to and extract extra condition for second table
            for index, resulting_state in enumerate(
                table_id_data[2:]
            ):  # resulting states start at index 2
                if isinstance(resulting_state, str):
                    break
            first_table_resulting_states = table_id_data[2 : index - 1]
            second_table_resulting_states = table_id_data[index + 1 :]
            second_table_extra_condition = table_id_data[index]

            # build first table
            prev_state_transition = None
            for resulting_state in first_table_resulting_states:

                new_state_transition = (
                    StateTransition.objects.create()
                )  # TODO set res later
                for patient_state in patient_states:
                    if patient_state["state_id"] == int(resulting_state):
                        data = patient_state["data"]
                        is_dead = patient_state["is_dead"]

                PatientState.objects.create(
                    state_id=int(resulting_state),
                    data=data,
                    is_dead=is_dead,
                )  # TODO: add transition

                root_node = LogicNode.objects.create(
                    state_transition=new_state_transition,
                    node_type=LogicNode.NodeType.AND,
                )
                for subcondition in table0:
                    subcondition_object = Subcondition.objects.get(name=subcondition)
                    LogicNode.objects.create(
                        state_transition=new_state_transition,
                        node_type=LogicNode.NodeType.SUBCONDITION,
                        subcondition=subcondition_object,
                        parent=root_node,
                    )
                # if there was a previous state transition, update it's next_state_transition to the current one to create linked list
                if prev_state_transition is not None:
                    prev_state_transition.next_state_transition = new_state_transition

                prev_state_transition = new_state_transition

                # if isinstance(resulting_state, int): # Beatmet is somewhere in there
                #     state_transition = StateTransition.objects.create() #TODO add resulting_state and next_state_transition

                # else:

        # assert len(row) == len(subconditions)
        # #TODO: link resulting_state and next_state_transition
        # state_transition = StateTransition.objects.create()
        # for i, field in enumerate(row):
        #     if field == "ja":
        #         # get subcondition for this field
        #         subcondition = Subcondition.objects.filter(name=subconditions[i])
        #         #TODO: link parent if exists
        #         LogicNode.objects.create(
        #             state_transition=state_transition,
        #             node_type=LogicNode.NodeType.SUBCONDITION,
        #             subcondition=subcondition,
        #         )

    # def get_resulting_state(self, tables):

    def parse_patient_data(self, patient_code):
        base_dir = os.path.join(settings.DATA_ROOT, "patient_states/")
        filename = str(patient_code) + "_transitions.csv"
        full_path = os.path.join(base_dir, filename)
        with open(full_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            field_names = []
            # go through first line to get all field names
            for field in next(reader):
                field_names.append(field)
            field_names = field_names[1:-1]  # remove "Status" and "Übergangstabelle"
            patient_states = []
            for row in reader:
                patient_state = {}
                row = [field.replace("|", "\n") for field in row]
                state_id = int(row[0])
                data = []
                i = 1
                for field in field_names:
                    d = {field: row[i]}
                    i += 1
                    data.append(d)
                data = json.dumps(data, sort_keys=True)
                is_dead = state_id == 500 or state_id == 502
                patient_state["state_id"] = state_id
                patient_state["data"] = data
                patient_state["is_dead"] = is_dead
                patient_state["table_id"] = row[-1]

                patient_states.append(patient_state)

        return patient_states
        # PatientState.objects.create(
        #     state_id=row[0],
        #     transition=transition,
        #     data=data,
        #     is_dead=is_dead,
        # )


# TODO: how do we check "freie Atemwege"? this doesn't depend on measures, instead its in the patient state data
# TODO: which action corresponds to "Infusion"?
# TODO: add action for Operation, then also add to corresponding Subcondition
# TODO: which action corresponds to "O2 Inhalation", same for O2?
# TODO: which action corresponds to "CPAP"?
# TODO: are there more "Blutstillungen" than "Chir. Blutstillung"?
# TODO: fix state_depth removal in patient_state_factory
