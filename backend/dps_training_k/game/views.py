from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from game.models import User

class PatientAccessView(APIView):
    def post(self, request, *args, **kwargs):
        user, created = User.objects.get_or_create(username='123')  # Ensure the username is a string
        if created:
            user.set_password("123")  # Properly hash the password
            user.save()
        if not (request.data.get("exerciseId") and request.data.get("patientId")):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Some required fields are missing",
            )
        exercise_code = request.data.get("exerciseId")
        patient_code = request.data.get("patientId")
        user = authenticate(username=exercise_code, password=patient_code)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
