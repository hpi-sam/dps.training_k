"""
ASGI config for dps_training_k project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from game.routing import application as channels_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dps_training_k.settings")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer

application = ProtocolTypeRouter(
    {
        # "http": django_asgi_app,
        "websocket": channels_application,
    }
)
