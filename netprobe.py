# Netprobe Service

import time
from helpers.network_helper import NetworkCollector
from helpers.http_helper import *
from helpers.redis_helper import *
from config import Config_Netprobe
from datetime import datetime
from helpers.logging_helper import *

if __name__ == '__main__':

    # Global Variables

    probe_interval = Config_Netprobe.probe_interval
    probe_count = Config_Netprobe.probe_count
    sites = Config_Netprobe.sites
    dns_test_site = Config_Netprobe.dns_test_site
    nameservers_external = Config_Netprobe.nameservers

    collector = NetworkCollector(sites,probe_count,dns_test_site,nameservers_external)

    # Logging Config

    logger = setup_logging("logs/netprobe.log")

    while True:
        
        try:
            stats = collector.collect()
            current_time = datetime.now()

        except Exception as e:
            print("Error testing network")
            logger.error("Error testing network")
            logger.error(e)
            continue

        # Connect to Redis

        try:

            cache = RedisConnect()

            # Save Data to Redis

            cache_interval = probe_interval + 15 # Set the redis cache TTL slightly longer than the probe interval

            cache.redis_write('netprobe',json.dumps(stats),cache_interval)

            #logger.info(f"Stats successfully written to Redis from device ID for Netprobe")

        except Exception as e:

            logger.error("Could not connect to Redis")
            logger.error(e)
        
        time.sleep(probe_interval)