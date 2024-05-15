# Data presentation service (prometheus)

import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import json
from helpers.redis_helper import *
from helpers.logging_helper import *
from config import Config_Presentation

# Logging config

logger = setup_logging("logs/presentation.log")

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):

        # Connect to Redis

        try:
            cache = RedisConnect()
        except Exception as e:
            logger.error("Could not connect to Redis")
            logger.error(e)

        if not cache:
            return

        # Retrieve Netprobe data

        results_netprobe = cache.redis_read('netprobe') # Get the latest results from Redis

        if results_netprobe:
            stats_netprobe = json.loads(json.loads(results_netprobe))
        else:
            return

        g = GaugeMetricFamily("Network_Stats", 'Network statistics for latency and loss from the probe to the destination', labels=['type','target'])

        total_latency = 0 # Calculate these in presentation rather than prom to reduce cardinality
        total_loss = 0
        total_jitter = 0

        for item in stats_netprobe['stats']: # Expose each individual latency / loss metric for each site tested

            g.add_metric(['latency',item['site']],item['latency'])
            g.add_metric(['loss',item['site']],item['loss'])
            g.add_metric(['jitter',item['site']],item['jitter'])            

        for item in stats_netprobe['stats']: # Aggregate all latency / loss metrics into one

            total_latency += float(item['latency'])
            total_loss += float(item['loss'])
            total_jitter += float(item['jitter'])

        average_latency = total_latency / len(stats_netprobe['stats'])
        average_loss = total_loss / len(stats_netprobe['stats'])
        average_jitter = total_jitter / len(stats_netprobe['stats'])

        g.add_metric(['latency','all'],average_latency)
        g.add_metric(['loss','all'],average_loss)
        g.add_metric(['jitter','all'],average_jitter)        

        yield g

        h = GaugeMetricFamily("DNS_Stats", 'DNS performance statistics for various DNS servers', labels=['server'])

        for item in stats_netprobe['dns_stats']:
            h.add_metric([item['nameserver']],item['latency'])

            if item['nameserver'] == 'My_DNS_Server':
                my_dns_latency = float(item['latency']) # Grab the current DNS latency of the probe's DNS resolver
    
        yield h

        # Retrieve Speedtest data

        results_speedtest = cache.redis_read('speedtest') # Get the latest results from Redis

        if results_speedtest: # Speed test is optional
            stats_speedtest = json.loads(json.loads(results_speedtest))

            s = GaugeMetricFamily("Speed_Stats", 'Speedtest performance statistics from speedtest.net', labels=['direction'])

            for key in stats_speedtest['speed_stats'].keys():
                if stats_speedtest['speed_stats'][key]:
                    s.add_metric([key],stats_speedtest['speed_stats'][key])
        
            yield s

        # Calculate overall health score

        weight_loss = Config_Presentation.weight_loss # Loss is 60% of score
        weight_latency = Config_Presentation.weight_latency # Latency is 15% of score
        weight_jitter = Config_Presentation.weight_jitter # Jitter is 20% of score
        weight_dns_latency = Config_Presentation.weight_dns_latency # DNS latency is 0.05 of score

        threshold_loss = Config_Presentation.threshold_loss # 5% loss threshold as max
        threshold_latency = Config_Presentation.threshold_latency # 100ms latency threshold as max
        threshold_jitter = Config_Presentation.threshold_jitter # 30ms jitter threshold as max
        threshold_dns_latency = Config_Presentation.threshold_dns_latency # 100ms dns latency threshold as max


        if average_loss / threshold_loss >= 1:
            eval_loss = 1
        else:
            eval_loss = average_loss / threshold_loss

        if average_latency / threshold_latency >= 1:
            eval_latency = 1
        else:
            eval_latency = average_latency / threshold_latency

        if average_jitter / threshold_jitter >= 1:
            eval_jitter = 1
        else:
            eval_jitter = average_jitter / threshold_jitter

        if my_dns_latency / threshold_dns_latency >= 1:
            eval_dns_latency = 1
        else:
            eval_dns_latency = my_dns_latency / threshold_dns_latency

        # Master scoring function

        score = 1 - weight_loss * (eval_loss) - weight_jitter * (eval_jitter) - weight_latency * (eval_latency) - weight_dns_latency * (eval_dns_latency)

        i = GaugeMetricFamily("Health_Stats", 'Overall internet health function')
        i.add_metric(['health'],score)

        yield i


if __name__ == '__main__':

    start_http_server(Config_Presentation.presentation_port,addr=Config_Presentation.presentation_interface)
    
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(15)