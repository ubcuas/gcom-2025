"""
WSGI config for gcom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application
import socketio

from websocket.views import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gcom.settings')
django.setup()

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)
