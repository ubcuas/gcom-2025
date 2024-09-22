"""
ASGI config for gcom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import socketio

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from websocket.sockets import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gcom.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": socketio.ASGIApp(sio, django_asgi_app),
})


