import csv
import os
import re
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand

from template.constants import ActionIDs, MaterialIDs
from template.models import PatientState, Subcondition, LogicNode, StateTransition

CUSTOM_MAXINT = 100000  # doesn't matter, people shouldn't be doing the same thing 100000 times anyway


class Command(BaseCommand):
    help = "Populates the database with patient states. Takes about 10min to complete"
    # this relies on patient_state.transition to be null=True and blank=True

    def handle(self, *args, **kwargs):
        self.create_subconditions()
        self.create_patient_states_and_transitions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added patient states to the database")
        )

    def create_subconditions(self):
        """
        name="Lyse", // name of subcondition
        upper_limit=CUSTOM_MAXINT, // maximum number of occurrences of fulfilling actions or fulfilling materials
        lower_limit=1, // minimum number of occurrences of fulfilling actions or fulfilling materials
        fulfilling_measures={
            "actions": [str(ActionIDs.LYSE_VERARBREICHEN)],
            "materials": [],
        }, // actions / materials that fulfill this subcondition. everything is or-connected. and-connection is not possible with current implementation
        """

        # corresponds to "Lyse"
        Subcondition.objects.update_or_create(
            name="Lyse",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.LYSE_VERARBREICHEN)],
                "materials": [],
            },
        )
        # corresponds to "4 EK´s"
        Subcondition.objects.update_or_create(
            name="4 EK´s",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=4,
            fulfilling_measures={
                "actions": [str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN)],
                "materials": [],
            },
        )
        # corresponds to "Infusion"
        Subcondition.objects.update_or_create(
            name="0-1l Infusion",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={
                "actions": [str(ActionIDs.VOLLELEKTROLYT)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="1-2l Infusion",
            upper_limit=1,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.VOLLELEKTROLYT)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="2-3l Infusion",
            upper_limit=2,
            lower_limit=2,
            fulfilling_measures={
                "actions": [str(ActionIDs.VOLLELEKTROLYT)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="3l-inf Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=3,
            fulfilling_measures={
                "actions": [str(ActionIDs.VOLLELEKTROLYT)],
                "materials": [],
            },
        )
        # corresponds to "2l Infusion"
        Subcondition.objects.update_or_create(
            name="2l Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=2,
            fulfilling_measures={
                "actions": [str(ActionIDs.VOLLELEKTROLYT)],
                "materials": [],
            },
        )
        # corresponds to "Thoraxdrainage/ Pleurapunktion"
        Subcondition.objects.update_or_create(
            name="Thoraxdrainage/ Pleurapunktion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [
                    str(ActionIDs.THORAXDRAINAGE),
                    str(ActionIDs.PLEURAPUNKTION),
                ],
                "materials": [],
            },
        )
        # corresponds to "Glucose"
        Subcondition.objects.update_or_create(
            name="Glucose",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.GLUCOSE_VERABREICHEN)],
                "materials": [],
            },
        )
        # corresponds to "Nitrat"
        Subcondition.objects.update_or_create(
            name="Nitrat",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={"actions": [str(ActionIDs.NITRAT)], "materials": []},
        )
        # corresponds to O2
        Subcondition.objects.update_or_create(
            name="O2",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [
                    str(ActionIDs.SAUERSTOFF_ANBRINGEN),
                    str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN),
                ],
                "materials": [],
            },
        )
        # corresponds to "OP läuft / ist gelaufen" as well as "keine OP"
        Subcondition.objects.update_or_create(
            name="OP läuft / ist gelaufen",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={"actions": [], "materials": []},
        )
        # corresponds to "Analgesie"
        Subcondition.objects.update_or_create(
            name="Analgesie",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.ANALGETIKUM)],
                "materials": [],
            },
        )
        # corresponds to "O2 Inhalation"
        Subcondition.objects.update_or_create(
            name="O2 Inhalation",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [
                    str(ActionIDs.SAUERSTOFF_ANBRINGEN),
                    str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN),
                ],
                "materials": [],
            },
        )
        # corresponds to "CPAP"
        Subcondition.objects.update_or_create(
            name="CPAP",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN)],
                "materials": [],
            },
        )
        # corresponds to "Antiasthmatikum"
        Subcondition.objects.update_or_create(
            name="Antiasthmatikum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.ANTIASTHMATIKUM)],
                "materials": [],
            },
        )
        # corresponds to "Sedativum"
        Subcondition.objects.update_or_create(
            name="Sedativum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.SEDATIVUM)],
                "materials": [],
            },
        )
        # corresponds to "freie Atemwege"
        Subcondition.objects.update_or_create(
            name="freie Atemwege",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [
                    str(ActionIDs.STABILE_SEITENLAGE),
                    str(ActionIDs.GUEDELTUBUS),
                    str(ActionIDs.WENDELTUBUS),
                    str(ActionIDs.TRACHEALTUBUS),
                    str(ActionIDs.LARYNXMASKE),
                    str(ActionIDs.LARYNXTUBUS),
                ],
                "materials": [],
            },
        )
        # corresponds to "EK´s"
        Subcondition.objects.update_or_create(
            name="0-1 EK´s",
            upper_limit=1,
            lower_limit=0,
            fulfilling_measures={
                "actions": [str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="2-3 EK´s",
            upper_limit=3,
            lower_limit=2,
            fulfilling_measures={
                "actions": [str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="4-5 EK´s",
            upper_limit=5,
            lower_limit=4,
            fulfilling_measures={
                "actions": [str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN)],
                "materials": [],
            },
        )
        Subcondition.objects.update_or_create(
            name="6-inf EK´s",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=6,
            fulfilling_measures={
                "actions": [str(ActionIDs.ERYTHROZYTENKONZENTRATE_ANWENDEN)],
                "materials": [],
            },
        )
        # corresponds to "Beatmet"
        Subcondition.objects.update_or_create(
            name="Beatmet",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.BEATMUNGSGERAET_ANBRINGEN)],
                "materials": [
                    str(MaterialIDs.BEATMUNGSGERAET_STATIONAER),
                    str(MaterialIDs.BEATMUNGSGERAET_TRAGBAR),
                ],
            },
        )
        # corresponds to Blutstillung
        Subcondition.objects.update_or_create(
            name="Blutstillung",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [str(ActionIDs.CHIR_BLUTSTILLUNG)],
                "materials": [],
            },
        )
        # corresponds to "Regional-/ Vollnarkose"
        Subcondition.objects.update_or_create(
            name="Regional-/ Vollnarkose",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={
                "actions": [
                    str(ActionIDs.REGIONAL_NARKOSE),
                    str(ActionIDs.REGIONAL_NARKOTIKUM),
                    str(ActionIDs.NARKOTIKUM),
                ],
                "materials": [],
            },
        )

    def create_patient_states_and_transitions(self):
        # outer loop to create all patients
        for code in range(1001, 1042):
            print("working on: ", code)
            self.code = code
            # parse data for specific patient
            self.patient_states = self.parse_patient_data(self.code)
            self.state_transitions = self.parse_state_transitions(self.code)
            # create starting state, then go into recursion to create other states and all transitions
            first_patient_state = self.patient_states[0]
            first_start_patient_state_obj, _ = PatientState.objects.get_or_create(
                code=self.code,
                state_id=first_patient_state["state_id"],
                vital_signs=first_patient_state["vital signs"],
                examination_codes=first_patient_state["examination codes"],
                special_events=first_patient_state["special events"],
                is_dead=first_patient_state["is_dead"],
            )
            first_state_transition = self.create_state_transitions(
                first_patient_state["table_id"]
            )[0]
            # finally, set the transition for the patient (first one of the linked list)
            first_start_patient_state_obj.transition = first_state_transition
            first_start_patient_state_obj.save()

            # create the other starting state, then go into recursion to create other states and all transitions
            for patient_state in self.patient_states:
                if int(patient_state["state_id"]) == 551:  # finds state data for id 551
                    break
            second_start_patient_state_obj, _ = PatientState.objects.get_or_create(
                code=self.code,
                state_id=patient_state["state_id"],
                vital_signs=patient_state["vital signs"],
                examination_codes=patient_state["examination codes"],
                special_events=patient_state["special events"],
                is_dead=patient_state["is_dead"],
            )
            first_state_transition = self.create_state_transitions(
                patient_state["table_id"]
            )[0]
            # finally, set the transition for the patient (first one of the linked list)
            second_start_patient_state_obj.transition = first_state_transition
            second_start_patient_state_obj.save()

    def create_patient_state(self, state_id):
        # find corresponding patient_state for state_id
        for patient_state in self.patient_states:
            if patient_state["state_id"] == int(state_id):
                break

        patient_state_obj, created = PatientState.objects.get_or_create(
            code=self.code,
            state_id=patient_state["state_id"],
            vital_signs=patient_state["vital signs"],
            examination_codes=patient_state["examination codes"],
            special_events=patient_state["special events"],
            is_dead=patient_state["is_dead"],
        )
        return patient_state_obj, created

    def create_state_transitions(self, table_id):
        for i, table_id_data in enumerate(self.state_transitions["table_results"]):
            if table_id_data["table_id"] == table_id:
                break
        relevant_table_id_data = self.state_transitions["table_results"][i]

        first_state_transition_table0 = None
        first_state_transition_table1 = None

        # guard condition "Immer" forces next state without any conditions
        if "Immer:" in relevant_table_id_data["extra_condition 1"]:
            first_state_transition_table0 = self.handle_guard_condition(
                relevant_table_id_data
            )
            first_state_transition_table1 = previous_state_transition = (
                first_state_transition_table0
            )

        else:
            if "keine Lyse:" in relevant_table_id_data["extra_condition 1"]:
                subcondition = Subcondition.objects.get(name="Lyse")
                first_state_transition_table0 = first_state_transition_table1 = (
                    self.handle_guard_condition(relevant_table_id_data, subcondition)
                )
            if "keine OP:" in relevant_table_id_data["extra_condition 1"]:
                subcondition = Subcondition.objects.get(name="OP läuft / ist gelaufen")
                first_state_transition_table0 = first_state_transition_table1 = (
                    self.handle_guard_condition(relevant_table_id_data, subcondition)
                )
            if "keine Blutstillung:" in relevant_table_id_data["extra_condition 1"]:
                subcondition = Subcondition.objects.get(name="Blutstillung")
                first_state_transition_table0 = first_state_transition_table1 = (
                    self.handle_guard_condition(relevant_table_id_data, subcondition)
                )

            # create transitions for table 0
            previous_state_transition = first_state_transition_table0
            table0 = self.state_transitions["table 0"]
            for i, line in enumerate(table0[1:]):  # for each line of the table
                resulting_state_id = int(relevant_table_id_data["table_0_results"][i])
                # end of recursion
                if resulting_state_id % 10 == 0 and resulting_state_id != 500:
                    state_transition_obj, _ = StateTransition.objects.get_or_create(
                        resulting_state=None
                    )
                    LogicNode.objects.get_or_create(
                        state_transition=state_transition_obj,
                        node_type=LogicNode.NodeType.TRUE,
                    )
                    return (state_transition_obj, state_transition_obj)

                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )

                # only go further into recursion if resulting state didn't exist before
                if created:
                    # get table_id for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            break

                    # recursive call to create transitions and resulting states for state created above
                    resulting_state_transition = self.create_state_transitions(
                        table_id
                    )[0]
                    resulting_patient_state_obj.transition = resulting_state_transition
                    resulting_patient_state_obj.save()

                # create transition to resulting state
                # transition needs to be assigned to PatientState object by caller
                state_transition, _ = StateTransition.objects.get_or_create(
                    resulting_state=resulting_patient_state_obj
                )
                self.create_logic_nodes(
                    deepcopy(table0),
                    deepcopy(relevant_table_id_data["extra_condition 1"]),
                    state_transition,
                    line,
                )  # deepcopy enforces pass by value which is necessary to prevent adding extra conditions multiple times
                # save first transition to return it later
                if not first_state_transition_table0:
                    first_state_transition_table0 = state_transition

                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                    previous_state_transition.save()
                previous_state_transition = state_transition

            # create transitions for table 1
            table1 = self.state_transitions["table 1"]
            for i, line in enumerate(table1[1:]):  # for each line of the table
                resulting_state_id = int(relevant_table_id_data["table_1_results"][i])
                # end of recursion
                if resulting_state_id % 10 == 0 and resulting_state_id != 500:
                    state_transition_obj, _ = StateTransition.objects.get_or_create(
                        resulting_state=None
                    )
                    LogicNode.objects.get_or_create(
                        state_transition=state_transition_obj,
                        node_type=LogicNode.NodeType.TRUE,
                    )
                    return (state_transition_obj, state_transition_obj)

                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )
                # only go further into recursion if resulting state didn't exist before
                if created:
                    # get table_id for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            break

                    # recursive call to create transitions and resulting states for state created above
                    resulting_state_transition = self.create_state_transitions(
                        table_id
                    )[0]
                    resulting_patient_state_obj.transition = resulting_state_transition
                    resulting_patient_state_obj.save()

                # create transition to resulting state
                # transition needs to be assigned to PatientState object by caller
                state_transition, _ = StateTransition.objects.get_or_create(
                    resulting_state=resulting_patient_state_obj
                )
                self.create_logic_nodes(
                    deepcopy(table1),
                    deepcopy(relevant_table_id_data["extra_condition 2"]),
                    state_transition,
                    line,
                )  # deepcopy enforces pass by value which is necessary to prevent adding extra conditions multiple times

                # save first transition to return it later
                if not first_state_transition_table1:
                    first_state_transition_table1 = state_transition

                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                    previous_state_transition.save()
                previous_state_transition = state_transition

            # handle cases where tables are empty
            # this is for empty table 0
            if len(table0[1:]) == 0:
                resulting_state_id = int(relevant_table_id_data["table_0_results"][0])
                # end of recursion
                if resulting_state_id % 10 == 0 and resulting_state_id != 500:
                    state_transition_obj, _ = StateTransition.objects.get_or_create(
                        resulting_state=None
                    )
                    LogicNode.objects.get_or_create(
                        state_transition=state_transition_obj,
                        node_type=LogicNode.NodeType.TRUE,
                    )
                    return (state_transition_obj, state_transition_obj)

                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )

                # only go further into recursion if resulting state didn't exist before
                if created:
                    # get table_id for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            break
                    resulting_state_transition = self.create_state_transitions(
                        table_id
                    )[0]
                    resulting_patient_state_obj.transition = resulting_state_transition
                    resulting_patient_state_obj.save()

                # create transition to resulting state
                # transition needs to be assigned to PatientState object by caller
                state_transition, _ = StateTransition.objects.get_or_create(
                    resulting_state=resulting_patient_state_obj
                )
                self.create_logic_nodes(
                    deepcopy(table0),
                    deepcopy(relevant_table_id_data["extra_condition 1"]),
                    state_transition,
                    [],
                )  # deepcopy enforces pass by value which is necessary to prevent adding extra conditions multiple times

                # save first transition to return it later
                if not first_state_transition_table0:
                    first_state_transition_table0 = state_transition

                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                    previous_state_transition.save()
                previous_state_transition = state_transition

            # empty table 1
            if len(table1[1:]) == 0:
                resulting_state_id = int(relevant_table_id_data["table_1_results"][0])
                # end of recursion
                if resulting_state_id % 10 == 0 and resulting_state_id != 500:
                    state_transition_obj, _ = StateTransition.objects.get_or_create(
                        resulting_state=None
                    )
                    LogicNode.objects.get_or_create(
                        state_transition=state_transition_obj,
                        node_type=LogicNode.NodeType.TRUE,
                    )
                    return (state_transition_obj, state_transition_obj)

                resulting_patient_state_obj, created = self.create_patient_state(
                    resulting_state_id
                )

                # only go further into recursion if resulting state didn't exist before
                if created:
                    # get table_id for next transition
                    for patient_state in self.patient_states:
                        if patient_state["state_id"] == int(resulting_state_id):
                            table_id = patient_state["table_id"]
                            break
                    resulting_state_transition = self.create_state_transitions(
                        table_id
                    )[0]

                    resulting_patient_state_obj.transition = resulting_state_transition
                    resulting_patient_state_obj.save()

                # create transition to resulting state
                # transition needs to be assigned to PatientState object by caller
                state_transition, _ = StateTransition.objects.get_or_create(
                    resulting_state=resulting_patient_state_obj
                )
                self.create_logic_nodes(
                    deepcopy(table1),
                    deepcopy(relevant_table_id_data["extra_condition 2"]),
                    state_transition,
                    [],
                )  # deepcopy enforces pass by value which is necessary to prevent adding extra conditions multiple times

                # save first transition to return it later
                if not first_state_transition_table1:
                    first_state_transition_table1 = state_transition

                # link transitions to linked list
                if previous_state_transition:
                    previous_state_transition.next_state_transition = state_transition
                    previous_state_transition.save()

                previous_state_transition = state_transition

        return (first_state_transition_table0, first_state_transition_table1)

    # Guard conditions can be "Immer", "keine OP", "keine Lyse", "keine Blutstillung"
    # "Immer" has no subcondition
    def handle_guard_condition(self, relevant_table_id_data, subcondition=None):
        match = re.search(r"\d+", relevant_table_id_data["extra_condition 1"])
        if match:
            resulting_state_id = int(match.group())
        else:
            print("something went wrong while trying to find resulting state id")

        resulting_patient_state_obj, created = self.create_patient_state(
            resulting_state_id
        )

        # only go further into recursion if resulting state didn't exist before
        if created:
            # get table_id for next transition
            for patient_state in self.patient_states:
                if patient_state["state_id"] == int(resulting_state_id):
                    table_id = patient_state["table_id"]
                    break

            # recursive call to create transitions and resulting states for state created above
            resulting_state_transition = self.create_state_transitions(table_id)[0]
            resulting_patient_state_obj.transition = resulting_state_transition
            resulting_patient_state_obj.save()

        # create transition to resulting state
        # transition needs to be assigned to PatientState object by caller
        state_transition, _ = StateTransition.objects.get_or_create(
            resulting_state=resulting_patient_state_obj
        )
        if subcondition is not None:
            parent_node, _ = LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.NOT,
            )
            LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.SUBCONDITION,
                subcondition=subcondition,
                parent=parent_node,
            )
        # This is the "Immer" case
        else:
            LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.TRUE,
            )
        return state_transition

    def create_logic_nodes(
        self, table, extra_conditions, state_transition, current_line
    ):
        table_subconditions = table[0]
        nodes = []
        table_lines = table[1:]
        if "Nicht beatmet" in extra_conditions:
            subcondition = Subcondition.objects.get(name="Beatmet")
            parent_node, _ = LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.NOT,
            )
            node, _ = LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.SUBCONDITION,
                subcondition=subcondition,
                parent=parent_node,
            )
            nodes.append(parent_node)
        elif "Beatmet" in extra_conditions:
            subcondition = Subcondition.objects.get(name="Beatmet")
            node, _ = LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.SUBCONDITION,
                subcondition=subcondition,
            )
            nodes.append(node)

        for i, entry in enumerate(current_line):
            # we only create subconditions for the ones that are true. creating ones for false is unnecessary
            if entry == "ja":
                try:
                    subcondition = Subcondition.objects.get(name=table_subconditions[i])
                except:
                    print(
                        f"found multiple Subconditions with name equals {table_subconditions[i]}"
                    )
                node, _ = LogicNode.objects.get_or_create(
                    state_transition=state_transition,
                    node_type=LogicNode.NodeType.SUBCONDITION,
                    subcondition=subcondition,
                )
                nodes.append(node)
            elif entry == "nein":
                pass
            # entry contains a value (may also contain chars, but these are never important)
            # these Subconditions are split into value ranges. therefore we also need to get the next higher value for an upper bound
            elif re.search(r"\d+", entry):
                match = re.search(r"\d+", entry)
                value = int(match.group())
                next_higher_value = self.find_next_higher_value(value, table_lines, i)
                subcondition_name = table_subconditions[i]
                if (
                    value >= 1000
                ):  # Infusion has values in thousands, we assume only 1000ml Infusion is possible
                    value = value // 1000
                try:
                    subcondition = Subcondition.objects.get(
                        name__contains=subcondition_name,
                        lower_limit=value,
                        upper_limit=next_higher_value - 1,
                    )
                except:
                    print(
                        f"couldn't find Subcondition, name: {subcondition_name}, lower limit: {value}, upper limit: {next_higher_value}"
                    )
                node, _ = LogicNode.objects.get_or_create(
                    state_transition=state_transition,
                    node_type=LogicNode.NodeType.SUBCONDITION,
                    subcondition=subcondition,
                )
                nodes.append(node)
        if len(nodes) > 1:
            root_node, _ = LogicNode.objects.get_or_create(
                state_transition=state_transition,
                node_type=LogicNode.NodeType.AND,
            )
            for node in nodes:
                node.parent = root_node
                node.save()

    def find_next_higher_value(self, current_value, table, line_index):
        for line in table:
            match = re.search(r"\d+", line[line_index])
            value = int(match.group())
            if value > int(current_value):
                if (
                    value >= 1000
                ):  # Infusion has values in thousands, we assume only 1000ml Infusion is possible
                    return value // 1000
                return value
        return CUSTOM_MAXINT + 1

    def parse_state_transitions(self, patient_code):
        base_dir = os.path.join(settings.DATA_ROOT, "patient_states/")
        filename = str(patient_code) + "_tables.csv"
        full_path = os.path.join(base_dir, filename)
        state_transitions = {}
        with open(full_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

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
                elif parsing_table_1 and "Table-Id" not in row[0]:
                    table_data = row
                    table1.append(table_data)

                # parse data of each table id
                if "Table-Id" in row[0]:
                    # creates 5 groups: table-id, extra conditions 1 (e.g. Nicht Beatmet), extra conditions 2 (e.g. Beatmet) and resulting states for both tables
                    match = re.search(
                        r"Table-Id:\s+(\d+)\s+([a-zA-Z0-9\s:']+)(.*)", row[0]
                    )
                    if match:
                        table_id_data = {}  # data for one table id
                        table_id = match.group(1)
                        table_id_data["table_id"] = table_id
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
                                if (
                                    "Beatmet" in resulting_state
                                ):  # "Beatmet is always present and the only thing in the second extra condition"
                                    break

                            # split at index of beatmet to separate resulting states for first and second table
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

                    table_results.append(table_id_data)

        if table0[0][0] == "leer":
            table0[0] = []

        if table1[0][0] == "leer":
            table1[0] = []

        state_transitions["table 0"] = table0
        state_transitions["table 1"] = table1
        state_transitions["table_results"] = table_results
        return state_transitions

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
                vital_signs = {}
                examination_codes = {}
                vital_signs_fields = [
                    "Airway",
                    "Breathing",
                    "Circulation",
                    "Bewusstsein",
                    "Pupillen",
                    "Psyche",
                    "Haut",
                ]
                examination_codes_fields = [
                    "BGA-Oxy",
                    "BGA-SBH",
                    "Hb",
                    "BZ",
                    "Gerinnung",
                    "Leber",
                    "Niere",
                    "Infarkt",
                    "Lactat",
                    "Rö-Extremitäten",
                    "Rö-Thorax",
                    "Trauma-CT",
                    "Ultraschall",
                    "EKG",
                    "ZVD",
                ]
                special_events_fields = ["Beschreibung"]

                # for each field (state_id) check which part of the data it belongs to
                i = 1
                for field in field_names:
                    if field in vital_signs_fields:
                        vital_signs.update({field: row[i]})
                    elif field in examination_codes_fields:
                        if (
                            row[i] != ""
                        ):  # empty strings can't be converted to int and are therefore ignored
                            examination_codes.update({field: int(row[i])})
                    elif field in special_events_fields:
                        special_events = row[i]
                    i += 1

                is_dead = state_id == 500 or state_id == 502
                patient_state["state_id"] = state_id
                patient_state["vital signs"] = vital_signs
                patient_state["examination codes"] = examination_codes
                patient_state["special events"] = special_events
                patient_state["is_dead"] = is_dead
                patient_state["table_id"] = row[-1]

                patient_states.append(patient_state)

        return patient_states


# TODO: add action for Operation, then also add to corresponding Subcondition
# TODO: which action corresponds to "CPAP"?
# TODO: are there more "Blutstillungen" than "Chir. Blutstillung"?
# TODO: patient 1036 has no value for ZVD
