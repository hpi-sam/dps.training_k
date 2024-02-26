from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PatientAccessViewTest(APITestCase):
    def test_patient_access_view_with_valid_data(self):
        url = reverse("patient-access")
        data = {
            "exerciseCode": "exercise_code_value",
            "patientCode": "patient_code_value",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_patient_access_view_with_missing_data(self):
        url = reverse("patient-access")
        data = {
            "exerciseCode": "exercise_code_value",
            # Missing 'patientCode'
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Some required fields are missing")

    def test_patient_access_view_with_invalid_data(self):
        url = reverse("patient-access")
        data = {
            # Missing both 'exerciseCode' and 'patientCode'
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Some required fields are missing")
