from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.authtoken.models import Token

from configuration import settings
from configuration.asgi import application
from template.models import PatientInformation
from ..models import PatientInstance, Exercise


class TestUtilsMixin:
    async def create_patient_communicator_and_authenticate(self):
        """Needs the patient_information management command to be run before."""
        self.exercise = await sync_to_async(Exercise.createExercise)()
        self.patient_information = await sync_to_async(PatientInformation.objects.get)(
            code=1004
        )
        self.patient = await sync_to_async(PatientInstance.objects.create)(
            name="Max Mustermann",
            static_information=self.patient_information,
            exercise=self.exercise,
            patient_frontend_id=settings.ID_GENERATOR.get_patient_frontend_id(),
        )
        self.token, _ = await sync_to_async(Token.objects.get_or_create)(
            user=self.patient.user
        )

        communicator = WebsocketCommunicator(
            application=application, path=f"/ws/patient/?token={self.token.key}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "Failed to connect to WebSocket")

        return communicator
