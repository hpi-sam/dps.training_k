from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import User


class PatientAccessView(APIView):
    def post(self, request, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="2"  # has to be the same as the username in abstract_consumer.py#authenticate
        )  # Ensure the username is a string
        if created:
            user.set_password("abcdef")  # Properly hash the password
            user.save()

        if not (request.data.get("exerciseId") and request.data.get("patientId")):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Some required fields are missing",
            )
        exercise_id = str(request.data.get("exerciseId"))
        patient_id = str(request.data.get("patientId"))

        user = authenticate(username=patient_id, password=exercise_id)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
