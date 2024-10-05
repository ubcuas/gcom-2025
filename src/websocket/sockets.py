from datetime import datetime, timedelta
from typing import Any, List, Mapping
from asgiref.sync import sync_to_async
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid: str, _: Mapping[str, Any]) -> None:
    """Runs whenever a client connects to the server

    Args:
        sid (str): The session ID of the connecting client
    """
    print(f"[SOCKET] Client Connected (SID={sid})")
    await sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)


@sio.event
async def disconnect(sid: str) -> None:
    """Runs whenever a client disconnects from the server

    Args:
        sid (str): The session ID of the disconnecting
    """
    print(f"[SOCKET] Client Disconnected (  SID={sid})")


@sio.on("message")
async def log_message(sid: str, *args: List[str]) -> None:
    """Runs whenever a message is sent to the server

    Args:
        sid (str): The session ID of the client sending the message
        *args (List[str]): The arguments of the message
    """
    print(f"[SOCKET] Message from {sid}: {args}")


@sio.on("ping")
async def ping(sid: str, _: dict = {}) -> None:
    """Runs whenever a client pings the server and emits a 'pong' event in response

    Args:
        sid (str): The session ID of the client pinging the server
    """
    print(f"[SOCKET] Ping from {sid}")
    await sio.emit("pong", room=sid)


@sio.on("drone_update")
async def drone_update(sid: str, data: dict) -> None:
    """
    Runs whenever the drone telemetry data is received
    Saves the telemetry data to the database and deletes records over 5 mins old

    Args:
        sid (str): The session ID of the client sending the update
        data (dict): The telemetry data of the drone
    """

    print(f"[SOCKET] Drone Update from {sid}: {data}")

    await sync_to_async(process_drone_update)(data)


def process_drone_update(data: dict) -> None:
    """
    Handles the synchronous processing of the drone update
    Saves the telemetry data to the database and deletes records over 5 mins old
    """
    from drone.models import DroneTelemetry
    from drone.serializers import DroneTelemetrySerializer

    # Validate telemetry data
    telemetry = DroneTelemetrySerializer(data=data)
    telemetry.is_valid(raise_exception=True)

    telemetry.save()

    # Drop records older than 5 minutes
    cutoff_time = (datetime.now() - timedelta(minutes=5)).timestamp()
    old_records = DroneTelemetry.objects.filter(timestamp__lt=int(cutoff_time))
    old_records.delete()
