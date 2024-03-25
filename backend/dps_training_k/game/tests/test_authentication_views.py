from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from game.models import User


class PatientAccessViewTest(APITestCase):
    def setUp(self):
        # Create a user that will attempt to log in
        self.test_user = User.objects.create_user("testuser", password="testpassword")
        self.test_user.save()

        # URL for the access view
        self.access_url = reverse("patient-access")

    def test_access_success(self):
        """
        Test the access with correct credentials.
        """
        data = {"exerciseId": "testuser", "patientId": "testpassword"}
        response = self.client.post(self.access_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response contains a token
        self.assertTrue("token" in response.data)

    def test_access_fail_wrong_credentials(self):
        """
        Test the access with wrong credentials.
        """
        data = {"exerciseId": "wronguser", "patientId": "wrongpassword"}
        response = self.client.post(self.access_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response indicates a failure
        self.assertTrue("error" in response.data)
        self.assertEqual(response.data["error"], "Wrong Credentials")

    def test_access_fail_missing_fields(self):
        """
        Test the access with missing fields.
        """
        data = {
            "exerciseId": "testuser"
            # Missing "patientId"
        }
        response = self.client.post(self.access_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response indicates missing fields
        self.assertTrue("Some required fields are missing" in response.data)
