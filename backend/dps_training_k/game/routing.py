from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from game.consumers import TrainerConsumer, PatientConsumer

websocket_urlpatterns = [
    path("rooms/<str:exercise_code>/trainer/", TrainerConsumer.as_asgi()),
    path("rooms/<str:exercise_code>/patient/<str:patient_code>", PatientConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(websocket_urlpatterns),
        # Add HTTP (and other protocols) here if needed
    }
)
