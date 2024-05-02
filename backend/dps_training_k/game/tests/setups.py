from unittest.mock import patch


class ResourcesDeactivateable:
    def deactivate_resources(self):
        self._consume_resources_patch_patient = patch(
            "game.models.PatientActionInstance._consume_resources"
        )
        self._consume_resources_patch_lab = patch(
            "game.models.LabActionInstance._consume_resources"
        )
        self._application_finished_strategy_patch_patient = patch(
            "game.models.PatientActionInstance._application_finished_strategy"
        )
        self._application_finished_strategy_patch_lab = patch(
            "game.models.LabActionInstance._application_finished_strategy"
        )
        self._consume_resources_patient = self._consume_resources_patch_patient.start()
        self._consume_resources_lab = self._consume_resources_patch_lab.start()
        self._application_finished_strategy_patient = (
            self._application_finished_strategy_patch_patient.start()
        )
        self._application_finished_strategy_lab = (
            self._application_finished_strategy_patch_lab.start()
        )
        self._consume_resources_patient.return_value = None
        self._consume_resources_lab.return_value = None
        self._application_finished_strategy_patient.return_value = None
        self._application_finished_strategy_lab.return_value = None

    def activate_resources(self):
        self._consume_resources_patch_patient.stop()
        self._consume_resources_patch_lab.stop()
        self._application_finished_strategy_patch_patient.stop()
        self._application_finished_strategy_patch_lab.stop()
