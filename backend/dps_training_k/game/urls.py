from .views import PatientAccessView
from django.urls import path

urlpatterns = [
    path("patient/access", PatientAccessView.as_view(), name="patient-access"),
]
