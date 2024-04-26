# Netprobe Lite

Simple and effective tool for measuring ISP performance at home. The tool measures several performance metrics including packet loss, latency, jitter, and DNS performance. It also aggregates these metrics into a common score, which you can use to monitor overall health of your internet connection.

## Requirements and Setup

To run Netprobe Lite, you'll need a PC running Docker connected directly to your ISP router. Specifically:

1. Netprobe Lite requires the latest version of Docker. For instructions on installing Docker, see YouTube, it's super easy.

2. Netprobe Lite should be installed on a machine (the 'probe') which has a wired Ethernet connection to your primary ISP router. This ensures the tests are accurately measuring your ISP performance and excluding and interference from your home network. An old PC with Linux installed is a great option for this.

## Installation

1. Clone the repo locally to the probe machine:

```
git clone https://github.com/plaintextpackets/netprobe_lite.git
```

2. From the cloned folder, use docker compose to launch the app:

```
docker compose up
```

3. To shut down the app, use docker compose again:

```
docker compose down
```

## How to use

1. Navigate to: http://x.x.x.x:3001/d/app/netprobe where x.x.x.x = IP of the probe machine running Docker.

2. Default user / pass is 'admin/admin'. Login to Grafana and set a custom password.

### Change Netprobe port

To change the port that Netprobe is running on, edit the 'compose.yml' file, under the 'grafana' section:

```    
ports:
    - '3001:3000'
```

Change the port on the left to the port you want to access Netprobe on

### Customize DNS test

If the DNS server your network uses is not already monitored, you can add your DNS server IP for testing.

To do so, modify this line in .env:

```
DNS_NAMESERVER_4_IP="8.8.8.8" # Replace this IP with the DNS server you use at home
```

Change 8.8.8.8 to the IP of the DNS server you use, then restart the application (docker compose down / docker compose up)

### Data storage

By default, Docker will store the data collected in a volume, which will persist between restarts.

To clear out old data, you need to first delete the Prometheus container:

```
docker rm netprobe-prometheus
```

Then prune the docker volumes:

```
docker volume prune
```

When started again the old data should be wiped out.

### Run on startup

To configure the tool to work as a daemon (run on startup, keep running), edit 'compose.yml' and add the following to each service:

```
restart: always
```

More information can be found in the Docker documentation.

## License

This project is released under a custom license that restricts commercial use. You are free to use, modify, and distribute the software for non-commercial purposes. Commercial use of this software is strictly prohibited without prior permission. If you have any questions or wish to use this software commercially, please contact [plaintextpackets@gmail.com].
