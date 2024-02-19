from django.urls import path
from game.consumers import TrainerConsumer, PatientConsumer

websocket_urlpatterns = [
    path("ws/trainer/", TrainerConsumer.as_asgi()),
    path("ws/patient/", PatientConsumer.as_asgi()),
]
