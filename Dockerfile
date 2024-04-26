FROM ubuntu:latest

COPY requirements.txt /netprobe_lite/requirements.txt

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apt-get update -y \ 
&& apt-get install -y python3 \ 
&& apt-get install -y python3-pip \ 
&& apt-get install -y iputils-ping \ 
&& pip install -r /netprobe_lite/requirements.txt --break-system-packages

WORKDIR /netprobe_lite

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]