# Dockerfile for netprobe_lite
# https://github.com/plaintextpackets/netprobe_lite/

# Default to arm32v7 if no build argument is provided
ARG BASE_IMAGE_ARCH=arm32v7

# Default to Python 3.12 if no build argument is provided
ARG PYTHON_VERSION=3.12

FROM ${BASE_IMAGE_ARCH}/python:${PYTHON_VERSION}-slim-bookworm

WORKDIR /netprobe_lite

# Copy application code
COPY src/ /netprobe_lite/

# Install python/pip
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y iputils-ping && apt-get install -y traceroute && apt-get clean \
    && pip install -r /netprobe_lite/requirements.txt --break-system-packages

# Make sure entrypoint.sh is executable
RUN chmod +x /netprobe_lite/entrypoint.sh

ENTRYPOINT [ "/bin/bash", "/netprobe_lite/entrypoint.sh" ]
