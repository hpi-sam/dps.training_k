from unittest.mock import patch


class ResourcesDeactivateable:
    def deactivate_resources(self):
        self._consume_resources_patch = patch(
            "game.models.ActionInstance._consume_resources"
        )
        self._return_applicable_resources_patch = patch(
            "game.models.ActionInstance._return_applicable_resources"
        )
        self._produce_resources_patch = patch(
            "game.models.ActionInstance._produce_resources"
        )
        self._consume_resources = self._consume_resources_patch.start()
        self._return_applicable_resources = (
            self._return_applicable_resources_patch.start()
        )
        self._produce_resources = self._produce_resources_patch.start()
        self._consume_resources.return_value = True
        self._return_applicable_resources.return_value = True
        self._produce_resources.return_value = True

    def activate_resources(self):
        self._consume_resources_patch.stop()
        self._return_applicable_resources_patch.stop()
        self._produce_resources_patch.stop()
