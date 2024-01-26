from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from game.consumers import TrainerConsumer, PatientConsumer

websocket_urlpatterns = [
    path("ws/trainer/", TrainerConsumer.as_asgi()),
    path("ws/patient/", PatientConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(websocket_urlpatterns),
        # Add HTTP (and other protocols) here if needed
    }
)
