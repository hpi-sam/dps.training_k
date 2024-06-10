from .views import PatientAccessView, TrainerLoginView
from django.urls import path

urlpatterns = [
    path("patient/access", PatientAccessView.as_view(), name="patient-access"),
    path("trainer/login", TrainerLoginView.as_view(), name="trainer-login")
]
