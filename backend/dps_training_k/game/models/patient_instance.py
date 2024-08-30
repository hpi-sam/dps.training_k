import re
from collections import defaultdict

from django.core.exceptions import ValidationError
from django.db import models

from configuration import settings
from game.models import Exercise
from game.channel_notifications import PatientInstanceDispatcher
from helpers.eventable import Eventable
from helpers.moveable import Moveable
from helpers.moveable_to import MoveableTo
from helpers.triage import Triage
from helpers.completed_actions import CompletedActionsMixin
from template.models import Patient, Action, Subcondition, Material

# from game.models import ActionInstanceStateNames moved into function to avoid circular imports

# from game.models import Area, Lab  # moved into function to avoid circular imports
# from game.models import ActionInstance, ActionInstanceStateNames  # moved into function to avoid circular imports

import logging

logger = logging.getLogger(__name__)

def validate_patient_frontend_id(value):
    if not re.fullmatch(r"^\d{6}$", value):
        raise ValidationError(
            "The patient_frontend_id must be a six-digit number, including leading zeros.",
            params={"value": value},
        )


class PatientInstance(
    CompletedActionsMixin, Eventable, Moveable, MoveableTo, models.Model
):
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Max Mustermann")
    frontend_id = models.CharField(
        max_length=6,
        unique=True,
        help_text="patient_frontend_id used to log into patient - see validator for format",
        validators=[validate_patient_frontend_id],
    )
    patient_template = models.ForeignKey(
        "template.Patient",
        on_delete=models.CASCADE,
    )
    patient_state_id = models.CharField(
        max_length=16,
        help_text="State of the patient",
    )
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )
    user = models.OneToOneField(
        "User",
        on_delete=models.SET_NULL,  # PatientInstance is deleted when user is deleted
        null=True,
        blank=True,
        help_text="User object for authentication - has to be deleted explicitly or manually",
    )

    @property
    def code(self):
        return self.patient_template.info.get('code', 0)

    def save(self, *args, **kwargs):
        from . import User

        _state_adding = False  # saves historic value of self._state.adding, as it is changed after saving
        if (
            self._state.adding
        ):  # _state.adding is True if the instance does not exist in the database, so it is a new instance
            logger.info(f"_state.adding is true -> Creating new patient {self.frontend_id}")
            self.user, _ = User.objects.get_or_create(
                username=self.frontend_id, user_type=User.UserType.PATIENT
            )
            self.user.set_password(
                self.exercise.frontend_id
            )  # Properly hash the password
            self.user.save()

            if not self.patient_state_id:
                self.patient_state_id = self.patient_template.get_initial_state_id()
            _state_adding = True

        changes = kwargs.get("update_fields", None)

        if (
            not self.pk or (changes and "patient_template" in changes)
        ) and self.triage is not self.patient_template.info.get("triage", Triage.UNDEFINED):
            self.triage = self.patient_template.info.get("triage", Triage.UNDEFINED)
            if changes:
                changes.append("triage")
        PatientInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

        if _state_adding and self.exercise.state == Exercise.StateTypes.RUNNING:
            # self.apply_pretreatments()
            self.schedule_state_change()
            logger.info(f"Scheduled state change for patient {self.frontend_id}")

    def delete(self, using=None, keep_parents=False):
        """Is only called when the patient explicitly deleted and not in an e.g. batch or cascade delete"""
        if self.user:
            self.user.delete()
        PatientInstanceDispatcher.delete_and_notify(self)
        
    def get_patient_state(self):
        return self.patient_template.get_state(self.patient_state_id)

    def apply_pretreatments(self):
        from game.models import ActionInstance

        for pretreatment, amount in self.patient_template.info.get("pretreatment").items():
            for _ in range(amount):
                kwargs = {}
                needed_arguments = ActionInstance.needed_arguments_create(pretreatment)
                for arg in needed_arguments:
                    if arg == "patient_instance":
                        kwargs[arg] = self
                    elif arg == "destination_area":
                        kwargs[arg] = self.area
                    elif arg == "lab":
                        kwargs[arg] = self.lab

                ActionInstance.create_in_success_state(template=pretreatment, **kwargs)

    def schedule_state_change(self, time_offset=0):
        from game.models import ScheduledEvent

        state_change_time = 600

        if self.patient_template.is_dead(self.patient_state_id):
            return False
        if self.patient_template.is_final_state(self.patient_state_id):
            return False
        ScheduledEvent.create_event(
            exercise=self.exercise,
            t_sim_delta=state_change_time + time_offset,
            method_name="execute_state_change",
            patient=self,
        )

    def execute_state_change(self):
        if self.patient_template.is_dead(self.patient_state_id) or self.patient_template.is_final_state(self.patient_state_id):
            raise Exception(
                f"Patient is dead or in final state, state change should have never been scheduled"
            )
        
        logger.info(f"Executing state change for patient {self.frontend_id}")
        future_state_id = self.patient_template.get_next_state_id(self.patient_state_id, self.check_action, self.check_material)

        if not future_state_id:
            logger.error(f"Patient {self.frontend_id} is in state {self.patient_state_id}, but there is no next state")
            return False
        self.patient_state_id = future_state_id
        self.save(update_fields=["patient_state_id"])
        self.schedule_state_change()
        return True
    
    def check_action(self, action, quantity):
        logger.info(f"Checking action {action} with quantity {quantity}")
        from game.models import ActionInstanceState

        # Fetch all action instances related to the patient
        action_instances = self.actioninstance_set.select_related("template").all()

        # Filter action instances to include only those in success states
        success_action_instances = [
            ai for ai in action_instances
            if ai.current_state.name in ActionInstanceState.success_states()
            and str(ai.template.uuid) == action
        ]
        logger.info(f"Success action instances: {success_action_instances}")
        return len(success_action_instances) >= quantity
    
    def check_material(self, material, quantity):
        materials = Material.objects.all()
        num_of_materials_assigned = len(self.material_assigned(materials.get(uuid=material)))
        return num_of_materials_assigned >= quantity

    def get_fulfilled_subconditions(self):
        from game.models import ActionInstanceState

        # Fetch all necessary data in a single query for performance
        action_instances = self.actioninstance_set.select_related("template").all()
        subconditions = Subcondition.objects.all()
        materials = Material.objects.all()

        # This dict approach is much faster than filter, hence we use this
        template_action_count = defaultdict(int)
        for action_instance in action_instances:
            if (
                action_instance.current_state.name
                in ActionInstanceState.success_states()
            ):
                template_action_count[str(action_instance.template.uuid)] += 1
        fulfilled_subconditions = set()

        for subcondition in subconditions:
            isActionFulfilled = False
            fulfilling_actions = subcondition.fulfilling_measures["actions"]
            # special handling for "freie Atemwege" because it depends on a vital_signs field
            if (
                subcondition.name == "freie Atemwege"
                and "freie Atemwege" in self.patient_state.vital_signs["Airway"]
            ):
                fulfilled_subconditions.add(subcondition)

            fulfillment_count = 0
            for action, fulfillment_value in fulfilling_actions.items():
                fulfillment_count += template_action_count[action] * fulfillment_value
            if (
                subcondition.lower_limit <= fulfillment_count
                and fulfillment_count <= subcondition.upper_limit
            ):
                isActionFulfilled = True

            isMaterialFulfilled = False
            fulfilling_materials = subcondition.fulfilling_measures["materials"]
            fulfillment_count = 0
            for material, fulfillment_value in fulfilling_materials.items():
                num_of_materials_assigned = len(
                    self.material_assigned(materials.get(uuid=material))
                )
                fulfillment_count += num_of_materials_assigned * fulfillment_value
            if (
                fulfillment_count
                and subcondition.lower_limit <= fulfillment_count
                and fulfillment_count <= subcondition.upper_limit
            ):
                isMaterialFulfilled = True

            if isActionFulfilled or isMaterialFulfilled:
                fulfilled_subconditions.add(subcondition)

        return fulfilled_subconditions

    @staticmethod
    def frontend_model_name():
        return "Patient*in"

    def can_receive_actions(self):
        return not (self.patient_template.is_dead(self.patient_state_id) or self.patient_template.is_final_state(self.patient_state_id))

    def is_blocked(self):
        from game.models import ActionInstance, ActionInstanceStateNames

        scheduled_actions_exists = (
            ActionInstance.objects.filter(
                patient_instance=self,
                current_state__name=ActionInstanceStateNames.IN_PROGRESS,
            )
            .exclude(template__location=Action.Location.LAB)
            .exists()
        )

        return scheduled_actions_exists

    @staticmethod
    def can_move_to_type(obj):
        from game.models import Area, Lab

        return isinstance(obj, Area) or isinstance(obj, Lab)

    def _perform_move(self, obj):
        """
        This may only be called after verifying that the movement is possible
        """
        from game.models import Area, Lab

        show_warning = self.materialinstance_set.exists() or self.personnel_set.exists()
        for material_instance in self.materialinstance_set.all():
            material_instance.try_moving_to(self.attached_instance())
        for personnel in self.personnel_set.all():
            personnel.try_moving_to(self.attached_instance())
        if isinstance(obj, Area):
            self.area = obj
            self.lab = None
        elif isinstance(obj, Lab):
            self.area = None
            self.lab = obj
        self.save(update_fields=["area", "lab"])

        return True, (
            "Warnung: Ressourcen wurden automatisch freigegeben" if show_warning else ""
        )

    def check_moving_to_hook(self, obj):
        from game.models import Area, Lab

        if isinstance(obj, Area):
            if self.area == obj:
                return False, "Patient*in ist bereits in diesem Bereich"
        elif isinstance(obj, Lab):
            if self.lab == obj:
                return False, "Patient*in ist bereits in diesem Labor"

        for material_instance in self.materialinstance_set.all():
            succeeded, message = material_instance.check_moving_to(
                self.attached_instance()
            )
            if not succeeded:
                return False, "Fehler beim Freigeben der Ressourcen: " + message
        for personnel in self.personnel_set.all():
            succeeded, message = personnel.check_moving_to(self.attached_instance())
            if not succeeded:
                return False, "Fehler beim Freigeben der Ressourcen: " + message
        return True, ""

    def attached_instance(self):
        return self.area or self.lab

    def is_absent(self):
        from game.models import ActionInstanceStateNames

        return self.actioninstance_set.filter(
            template__relocates=True,
            current_state__name=ActionInstanceStateNames.IN_PROGRESS,
        ).exists()

    def __str__(self):
        return (
            f"Patient #{self.id} called {self.name} with frontend ID {self.frontend_id}"
        )
