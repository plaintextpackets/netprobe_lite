# Dockerfile for netprobe_lite
# https://github.com/plaintextpackets/netprobe_lite/
FROM python:3.11-slim-bookworm

COPY requirements.txt /netprobe_lite/requirements.txt

# Install python/pip
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y iputils-ping && apt-get install -y traceroute && apt-get clean \
    && pip install -r /netprobe_lite/requirements.txt --break-system-packages

WORKDIR /netprobe_lite

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]
