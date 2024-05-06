from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class PatientAccessView(APIView):
    def post(self, request, *args, **kwargs):
        if not (request.data.get("exerciseId") and request.data.get("patientId")):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Some required fields are missing",
            )
        exercise_frontend_id = str(request.data.get("exerciseId"))
        patient_frontend_id = str(request.data.get("patientId"))

        user = authenticate(username=patient_frontend_id, password=exercise_frontend_id)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
