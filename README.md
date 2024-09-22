# GCOM

TODO: Make this better

## Poetry
This project uses `poetry`. To install poetry, follow the guide on the website. Then run:
`poetry install` to install required dependencies. Some relavent commands you may want to know:
- `poetry shell` - Spawns and activates the poetry venv. Run `exit` to exit the venv
- `poetry add <module>` - Add a dependency
- `poetry remove <module>` - Remove a dependency
- `poetry run <command>` - Run a command in the poetry venv without activating it


## Overview
- Django + DRF: For ORM and API
- Django Channels (Daphne): For WebSocket support (not socketio)
- Celery for multitasking
