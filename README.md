# Netprobe

Simple and effective tool for measuring ISP performance at home. The tool measures several performance metrics including packet loss, latency, jitter, and DNS performance. It also has an optional speed test to measure bandwidth. Netprobe aggregates these metrics into a common score, which you can use to monitor overall health of your internet connection.

## Support the Project

If you'd like to support the development of this project, feel free to buy me a coffee!

https://buymeacoffee.com/plaintextpm

## Full Tutorial

Visit YouTube for a full tutorial on how to install and use Netprobe:

https://youtu.be/Wn31husi6tc


## Requirements and Setup

To run Netprobe, you'll need a PC running Docker connected directly to your ISP router. Specifically:

1. Netprobe requires the latest version of Docker. For instructions on installing Docker, see YouTube, it's super easy.

2. Netprobe should be installed on a machine (the 'probe') which has a wired Ethernet connection to your primary ISP router. This ensures the tests are accurately measuring your ISP performance and excluding and interference from your home network. An old PC with Linux installed is a great option for this.

## Installation

### First-time Install

1. Clone the repo locally to the probe machine:

```shell
git clone https://github.com/plaintextpackets/netprobe_lite.git
```

2. From the cloned folder, use docker compose to launch the app:

```shell
docker-compose -f docker-compose.yml -f example.docker-compose.override.yml up --build
```

3. To shut down the app, use docker compose again:

```shell
docker compose down
```

### Developers, Build and Publish to hub.Docker.com

Used environment variables in the Dockerfile
* `DOCKER_REGISTRY` # https://hub.docker.com/repository/docker/$DOCKER_REGISTRY
* `BASE_IMAGE_ARCH` # arm32v7
* `PYTHON_VERSION`  # 3.12

1. After finished the development locally.
2. Edit the `build.env` file with your info.

```shell
source build.env
```

1. Builds multi arch manifest including
- `amd64`
- `arm32v7`
- `arm64v8`
2. Then publishes them to the given `$DOCKER_REGISTRY` with `latest` tag.

```shell
./build_publish.sh
```

### Portrainer support

1. Checkout the repo for a given path (linux /project/)
1. Navigate to Portrainer
2. Open up Stack
3. (+) Add Stack
4. Choose Web Editor (using `docker-compose.yml`, since `docker-compose.override.yml` is not supported we have to create a workaround)

Use the following `docker-compose.yml`
```yml
# Docker compose file for netprobe
# https://github.com/xian55/netprobe_lite
name: netprobe

networks:
  netprobe-net:

services:
  redis:
    restart: always
    container_name: netprobe-redis
    image: "redis:latest"
    volumes:
      - /{REPLACE_ME}/config/redis/:/etc/redis/
      - /{REPLACE_ME}/logs:/logs
    networks:
      - netprobe-net
    env_file:
      - stack.env
    dns:
      - 8.8.8.8
      - 8.8.4.4

  netprobe:
    restart: always
    container_name: netprobe-probe
    image: "${DOCKER_REGISTRY}:latest"
    environment:
      MODULE: "NETPROBE"
    volumes:
      - /{REPLACE_ME}/logs:/logs
    env_file:
      - stack.env
    networks:
      - netprobe-net
    dns:
      - 8.8.8.8
      - 8.8.4.4

  speedtest:
    restart: always
    container_name: netprobe-speedtest
    image: "${DOCKER_REGISTRY}:latest"
    environment:
      MODULE: "SPEEDTEST"
    env_file:
      - stack.env
    volumes:
      - /{REPLACE_ME}/logs:/logs
    networks:
      - netprobe-net
    dns:
      - 8.8.8.8
      - 8.8.4.4

  presentation:
    restart: always
    container_name: netprobe-presentation
    image: "${DOCKER_REGISTRY}:latest"
    environment:
      MODULE: "PRESENTATION"
    env_file:
      - stack.env
    networks:
      - netprobe-net
    volumes:
      - /{REPLACE_ME}/logs:/logs
    dns:
      - 8.8.8.8
      - 8.8.4.4

  prometheus:
    restart: always
    container_name: netprobe-prometheus
    image: "prom/prometheus"
    env_file:
      - stack.env
    volumes:
      - /{REPLACE_ME}/logs:/logs
      - /{REPLACE_ME}/config/prometheus/:/etc/prometheus/
      - prometheus_data:/prometheus # Persistent local storage for Prometheus data
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - netprobe-net
    dns:
      - 8.8.8.8
      - 8.8.4.4

  grafana:
    restart: always
    image: grafana/grafana-enterprise
    container_name: netprobe-grafana
    env_file:
      - stack.env
    volumes:
      - /{REPLACE_ME}/logs:/logs
      - /{REPLACE_ME}/config/grafana/datasources/:/etc/grafana/provisioning/datasources/
      - /{REPLACE_ME}/config/grafana/dashboards/:/etc/grafana/provisioning/dashboards/
      - /{REPLACE_ME}/config/grafana/dashboards/:/var/lib/grafana/dashboards/
      - grafana_data:/var/lib/grafana
    ports:
      - '3001:3000'
    networks:
      - netprobe-net
    dns:
      - 8.8.8.8
      - 8.8.4.4

volumes:
  prometheus_data:
  grafana_data:
```

5. It is really important to set the `env_file` thats how you can pass the environment variables to the containers
```yml
    env_file:
      - stack.env
```

6. You might have noticed two baked in variables while mounting from the host machine
* `/{REPLACE_ME}/config`
* `/{REPLACE_ME}/logs`

7. Replace these what you like on your host machine, example: `/project/config` and `/project/logs`
8. Then i suggest load the `.env` file using the `Load variables from .env file` button
9. Lastly create a new `custom.env` file and place there all the changes what you wish to make over the base `.env` file
10. Then once again load the `custom.env` file using the `Load variables from .env file` button
11. You should be able to see the environment variables loaded, you may notice that the `custom.env` duplicated what you want to override.
12. Be sure to delete those environment variable keys which you want to overwrite.
13. Then finally press the `Update the stack` button.
14. The Containers should come online.

### Upgrading Between Versions

When upgrading between versions, it is best to delete the deployment altogether and restart with the new code. The process is described below.

1. Stop Netprobe in Docker and use the -v flag to delete all volumes (warning this deletes old data):

```shell
docker compose down -v
```

2. Clone the latest code (or download manually from Github and replace the current files):

```shell
git clone https://github.com/plaintextpackets/netprobe_lite.git
```

3. Re-start Netprobe:

```shell
docker-compose -f docker-compose.yml -f example.docker-compose.override.yml up
```

## How to use

1. Navigate to: http://x.x.x.x:3001/d/app/netprobe where x.x.x.x = IP of the probe machine running Docker.

2. Default user / pass is 'admin/admin'. Login to Grafana and set a custom password.

## How to customize

### Enable Speedtest

By default the speed test feature is disabled as many users pay for bandwidth usage (e.g. cellular connections). To enable it, edit the .env file to set the option to 'True':

```shell
SPEEDTEST_ENABLED="True"
```

Note: speedtest.net has a limit on how frequently you can connection and run the test. If you set the test to run too frequently, you will receive errors. Recommend leaving the 'SPEEEDTEST_INTERVAL' unchanged.

### Change Netprobe port

To change the port that Netprobe Lite is running on, edit the 'compose.yml' file, under the 'grafana' section:

```shell
ports:
    - '3001:3000'
```

Change the port on the left to the port you want to access Netprobe Lite on

### Customize DNS test

If the DNS server your network uses is not already monitored, you can add your DNS server IP for testing.

To do so, modify this line in .env:

```shell
DNS_NAMESERVER_4_IP="8.8.8.8" # Replace this IP with the DNS server you use at home
```

Change 8.8.8.8 to the IP of the DNS server you use, then restart the application (docker compose down / docker compose up)

### Use external Grafana

Some users have their own Grafana instance running and would like to ingest Netprobe statistics there rather than running Grafana in Docker. To do this:

1. In the docker-compose.yaml file, add a port mapping to the Prometheus deployment config:

```yaml
  prometheus:
    ...
    ports:
      - 'XXXX:9090'    
```
... where XXXX is the port you wish to expose Prometheus on your host machine

2. Remove all of the Grafana configuration from the compose.yaml file

3. Run Netprobe and then add a datasource to your existing Grafana as http://x.x.x.x:XXXX where x.x.x.x = IP of the probe machine running Docker

### Data storage - default method

By default, Docker will store the data collected in several Docker volumes, which will persist between restarts.

They are:

```shell
netprobe_grafana_data (used to store Grafana user / pw)
netprobe_prometheus_data (used to store time series data)
```

To clear out old data, you need to stop the app and remove these volumes:

```shell
docker compose down
docker volume rm netprobe_grafana_data
docker volume rm netprobe_prometheus_data
```

When started again the old data should be wiped out.

### Data storage - bind mount method

Using the default method, the data is stored within Docker volumes which you cannot easily access from the host itself. If you'd prefer storing data in mapped folders from the host, follow these instructions (thank you @Jeppedy):

1. Clone the repo

2. Inside the folder create two directories:

```shell
mkdir -p data/grafana data/prometheus 
```

3. Modify the `docker-compose.yml` as follows (volume path as well as adding user ID):

```yaml
  prometheus:
    restart: always
    container_name: netprobe-prometheus
    image: "prom/prometheus"
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./data/prometheus:/prometheus # modify this to map to the folder you created

    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - custom_network  # Attach to the custom network
    user: "1000" # set this to the desired user with correct permissions to the bind mount

  grafana:
    restart: always
    image: grafana/grafana-enterprise
    container_name: netprobe-grafana
    volumes:
      - ./config/grafana/datasources/automatic.yml:/etc/grafana/provisioning/datasources/automatic.yml
      - ./config/grafana/dashboards/main.yml:/etc/grafana/provisioning/dashboards/main.yml
      - ./config/grafana/dashboards/netprobe.json:/var/lib/grafana/dashboards/netprobe.json
      - ./data/grafana:/var/lib/grafana  # modify this to map to the folder you created
    ports:
      - '3001:3000'
    networks:
      - custom_network  # Attach to the custom network
    user: "1000" # set this to the desired user with correct permissions to the bind mount
```

4. Remove the volumes section from compose.yml


### Run on startup

Netprobe will automatically restart itself after the host system is rebooted, provided that Docker is also launched on startup. If you want to disable this behavior, modify the 'restart' variables in the compose.yaml file to this: 

```yaml
restart: never
```

### Wipe all stored data

To wipe all stored data and remove the Docker volumes, use this command:

```shell
docker compose down -v
```
This will delete all containers and volumes related to Netprobe.



## FAQ & Troubleshooting

Q. How do I reset my Grafana password?

A. Delete the docker volume for grafana. This will reset your password but will leave your data:

```shell
docker volume rm netprobe_grafana_data
```

Q. I am running Pihole and when I enter my host IP under 'DNS_NAMESERVER_4_IP=' I receive this error:

```
The resolution lifetime expired after 5.138 seconds: Server Do53:192.168.0.91@53 answered got a response from ('172.21.0.1', 53) instead of ('192.168.0.91', 53)
```
A. This is a limitation of Docker. If you are running another DNS server in Docker and want to test it in Netprobe, you need to specify the Docker network gateway IP:

1. Stop netprobe but don't wipe it (docker compose down)
2. Find the gateway IP of your netprobe-probe container:
```shell
$ docker inspect netprobe-probe | grep Gateway
            "Gateway": "",
            "IPv6Gateway": "",
                    "Gateway": "192.168.208.1",
                    "IPv6Gateway": "", 
```
3. Enter that IP (e.g. 182.168.208.1) into your .env file for 'DNS_NAMESERVER_4_IP='

Q. I constantly see one of my DNS servers at 5s latency, is this normal?

A. 5s is the timeout for DNS queries in Netprobe Lite. If you see this happening for one specific IP, likely your machine is having issues using that DNS server (and so you shouldn't use it for home use).

## License

This project is released under a custom license that restricts commercial use. You are free to use, modify, and distribute the software for non-commercial purposes. Commercial use of this software is strictly prohibited without prior permission. If you have any questions or wish to use this software commercially, please contact [plaintextpackets@gmail.com].
