FROM python:3.10

RUN apt-get update && apt-get install -y \
    redis-server \
    supervisor \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /src /var/log/supervisor

WORKDIR /src

COPY ./src /src
COPY pyproject.toml /src

# Install poetry using pip
RUN pip install poetry==1.7.1

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

RUN cat <<EOF > /etc/supervisor/supervisord.conf
[supervisord]
nodaemon=true

[program:redis]
command=redis-server
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/redis_stdout.log
stderr_logfile=/var/log/supervisor/redis_stderr.log

[program:server]
command=poetry run python server.py
directory=/src
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/server_stdout.log
stderr_logfile=/var/log/supervisor/server_stderr.log

[program:celery]
command=poetry run python -m celery -A gcom worker
directory=/src
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/celery_stdout.log
stderr_logfile=/var/log/supervisor/celery_stderr.log
EOF

EXPOSE 6379
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
