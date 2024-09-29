FROM python:3.12

RUN apt-get update && apt-get install -y \
    redis-server \
    supervisor \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /src /var/log/supervisor

WORKDIR /src

COPY ./src /src
COPY pyproject.toml /src

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

RUN echo "[supervisord]" > /etc/supervisor/supervisord.conf && \
    echo "nodaemon=true" >> /etc/supervisor/supervisord.conf && \
    echo "[program:redis]" >> /etc/supervisor/supervisord.conf && \
    echo "command=redis-server" >> /etc/supervisor/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisor/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisor/supervisord.conf && \
    echo "stdout_logfile=/var/log/supervisor/redis_stdout.log" >> /etc/supervisor/supervisord.conf && \
    echo "stderr_logfile=/var/log/supervisor/redis_stderr.log" >> /etc/supervisor/supervisord.conf && \
    echo "[program:server]" >> /etc/supervisor/supervisord.conf && \
    echo "command=poetry run python server.py" >> /etc/supervisor/supervisord.conf && \
    echo "directory=/src" >> /etc/supervisor/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisor/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisor/supervisord.conf && \
    echo "stdout_logfile=/var/log/supervisor/server_stdout.log" >> /etc/supervisor/supervisord.conf && \
    echo "stderr_logfile=/var/log/supervisor/server_stderr.log" >> /etc/supervisor/supervisord.conf && \
    echo "[program:celery]" >> /etc/supervisor/supervisord.conf && \
    echo "command=poetry run python -m celery -A gcom worker" >> /etc/supervisor/supervisord.conf && \
    echo "directory=/src" >> /etc/supervisor/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisor/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisor/supervisord.conf && \
    echo "stdout_logfile=/var/log/supervisor/celery_stdout.log" >> /etc/supervisor/supervisord.conf && \
    echo "stderr_logfile=/var/log/supervisor/celery_stderr.log" >> /etc/supervisor/supervisord.conf

EXPOSE 6379

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]