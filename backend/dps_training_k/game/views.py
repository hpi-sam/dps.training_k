from rest_framework.views import APIView
from game.models import User
from rest_framework import status
from rest_framework.response import Response


class PatientAccessView(APIView):
    def post(self, request, *args, **kwargs):
        if not (request.data.get("exerciseCode") and request.data.get("patientCode")):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Some required fields are missing",
            )

        new_patient = User.objects.create(
            username=request.data.get("exerciseCode"),
            user_type=User.UserType.PATIENT,
        )
        new_patient.set_password(request.data.get("patientCode"))

        return Response(
            status=status.HTTP_201_CREATED,
            data={"token": str(new_patient.auth_token.key)},
        )
