from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from game.models import User


class PatientAccessViewTest(APITestCase):
    def setUp(self):
        # Create a user that will attempt to log in
        self.test_user = User.objects.create_user("testuser", password="testpassword")
        self.test_user.save()

        # URL for the login view
        self.login_url = reverse("patient-access")

    def test_login_success(self):
        """
        Test the login with correct credentials.
        """
        data = {"exerciseCode": "testuser", "patientCode": "testpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response contains a token
        self.assertTrue("token" in response.data)

    def test_login_fail_wrong_credentials(self):
        """
        Test the login with wrong credentials.
        """
        data = {"exerciseCode": "wronguser", "patientCode": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response indicates a failure
        self.assertTrue("error" in response.data)
        self.assertEqual(response.data["error"], "Wrong Credentials")

    def test_login_fail_missing_fields(self):
        """
        Test the login with missing fields.
        """
        data = {
            "exerciseCode": "testuser"
            # Missing "patientCode"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response indicates missing fields
        self.assertTrue("Some required fields are missing" in response.data)
