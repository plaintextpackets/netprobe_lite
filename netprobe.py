# Netprobe service

import time
from helpers.network_helper import *
from helpers.http_helper import *
from helpers.redis_helper import *
from dotenv import load_dotenv
import os
from config import Config_Netprobe
from datetime import datetime,timezone
from helpers.logging_helper import *

if __name__ == '__main__':

    # Global Variables

    probe_interval = Config_Netprobe.probe_interval
    probe_count = Config_Netprobe.probe_count
    sites = Config_Netprobe.sites
    device_id = Config_Netprobe.device_id
    site_id = Config_Netprobe.site_id
    dns_test_site = Config_Netprobe.dns_test_site
    nameservers_external = Config_Netprobe.nameservers


    collector = NetworkCollector(sites,probe_count,device_id,site_id,dns_test_site,nameservers_external)
    sendhome = CallHome()

    # Logging config

    logger = setup_logging("logs/netprobe.log")


    while True:
        
        try:
            stats = collector.collect()
            current_time = datetime.now()

        except:
            print("Error testing network")
            logger.error("Error testing network")
            continue

        # Connect to Redis

        try:

            cache = RedisConnect()

            # Save data to Redis

            cache.redis_write(device_id,json.dumps(stats),45) # Store data with TTL 45s, which means when the probe goes down the key ages out

            logger.info(f"Stats successfully written to Redis from device ID {device_id}")

        except Exception as e:

            logger.error("Could not connect to Redis")
            logger.debug(exc_info=1)
        
        time.sleep(probe_interval)