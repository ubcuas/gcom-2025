# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'threading'
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gcom.settings')
django.setup()

import json
import datetime
from django.http import HttpResponse
from django.utils import timezone
import socketio

from drone.models import DroneTelemetry

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)


def index(request):
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


@sio.event
def connect(sid, environ):
    print(f"[SOCKET] Client Connected (SID={sid})")
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
def disconnect(sid):
    print(f"[SOCKET] Client Disconnected (SID={sid})")

@sio.on('drone_update')
def drone_telemetry_update(sid, data):
    data_json = json.loads(data)
    drone = DroneTelemetry(
        timestamp=data_json['timestamp'],
        latitude=data_json['latitude'],
        longitude=data_json['longitude'],
        altitude=data_json['altitude'],
        vertical_speed=data_json['vertical_velocity'],
        speed=data_json['velocity'],
        heading=data_json['heading'],
        battery_voltage=data_json['battery_voltage']
    )
    drone.save()