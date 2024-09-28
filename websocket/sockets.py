from typing import List
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid: str) -> None:
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
