from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class PatientAccessView(APIView):
    def post(self, request, *args, **kwargs):
        if not (request.data.get("exerciseCode") and request.data.get("patientId")):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Some required fields are missing",
            )
        exercise_code = request.data.get("exerciseCode")
        patient_code = request.data.get("patientId")
        user = authenticate(username=exercise_code, password=patient_code)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
