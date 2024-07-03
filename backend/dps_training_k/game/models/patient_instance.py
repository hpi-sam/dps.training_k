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
from template.models import PatientState, Action, Subcondition, Material

# from game.models import ActionInstanceStateNames moved into function to avoid circular imports

# from game.models import Area, Lab  # moved into function to avoid circular imports
# from game.models import ActionInstance, ActionInstanceStateNames  # moved into function to avoid circular imports


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
    patient_state = models.ForeignKey(
        "template.PatientState",
        on_delete=models.SET_NULL,
        null=True,  # for debugging purposes
        default=None,  # for debugging purposes
    )
    static_information = models.ForeignKey(
        "template.PatientInformation",
        on_delete=models.CASCADE,
        null=True,  # for migration purposes
    )  # via Sensen ID
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
        return self.static_information.code

    def save(self, *args, **kwargs):
        from . import User

        _state_adding = False  # saves historic value of self._state.adding, as it is changed after saving
        if (
            self._state.adding
        ):  # _state.adding is True if the instance does not exist in the database, so it is a new instance
            self.user, _ = User.objects.get_or_create(
                username=self.frontend_id, user_type=User.UserType.PATIENT
            )
            self.user.set_password(
                self.exercise.frontend_id
            )  # Properly hash the password
            self.user.save()

            if not self.patient_state:
                self.patient_state = PatientState.objects.get(
                    code=self.static_information.code,
                    state_id=self.static_information.start_status,
                )
            _state_adding = True

        changes = kwargs.get("update_fields", None)

        if (
            not self.pk or (changes and "static_information" in changes)
        ) and self.triage is not self.static_information.triage:
            self.triage = self.static_information.triage
            if changes:
                changes.append("triage")
        PatientInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

        if _state_adding and self.exercise.state == Exercise.StateTypes.RUNNING:
            self.apply_pretreatments()
            self.schedule_state_change()

    def delete(self, using=None, keep_parents=False):
        """Is only called when the patient explicitly deleted and not in an e.g. batch or cascade delete"""
        if self.user:
            self.user.delete()
        PatientInstanceDispatcher.delete_and_notify(self)

    def apply_pretreatments(self):
        from game.models import ActionInstance

        for pretreatment, amount in self.static_information.get_pretreatments().items():
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

        if self.patient_state.is_dead:
            return False
        if self.patient_state.is_final():
            return False
        ScheduledEvent.create_event(
            exercise=self.exercise,
            t_sim_delta=state_change_time + time_offset,
            method_name="execute_state_change",
            patient=self,
        )

    def execute_state_change(self):
        if self.patient_state.is_dead or self.patient_state.is_final():
            raise Exception(
                f"Patient is dead or in final state, state change should have never been scheduled"
            )
        fulfilled_subconditions = self.get_fulfilled_subconditions()
        future_state = self.patient_state.transition.activate(fulfilled_subconditions)
        if not future_state:
            return False
        self.patient_state = future_state
        self.save(update_fields=["patient_state"])
        self.schedule_state_change()
        return True

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
        return not (self.patient_state.is_dead or self.patient_state.is_final())

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
