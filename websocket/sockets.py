import socketio

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*"
)


@sio.event
async def connect(sid, environ):
    print(f"[SOCKET] Client Connected (SID={sid})")
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"[SOCKET] Client Disconnected (  SID={sid})")

# Print the message to the console
@sio.on("message")
async def log_message(sid, *args):
    print(f"[SOCKET] Message from {sid}: {args}")