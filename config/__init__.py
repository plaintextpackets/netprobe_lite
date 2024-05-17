import os
from dotenv import load_dotenv

# Load configs from env

try: # Try to load env vars from file, if fails pass
    load_dotenv()
except:
    pass


# Create class for each

class Config_Netprobe():
    probe_interval = int(os.getenv('PROBE_INTERVAL'))
    probe_count = int(os.getenv('PROBE_COUNT'))
    sites = os.getenv('SITES').split(',')
    dns_test_site = os.getenv('DNS_TEST_SITE')
    speedtest_enabled = os.getenv("SPEEDTEST_ENABLED", 'False').lower() in ('true', '1', 't')
    speedtest_interval = int(os.getenv('SPEEDTEST_INTERVAL'))

    DNS_NAMESERVER_1 = os.getenv('DNS_NAMESERVER_1')
    DNS_NAMESERVER_1_IP = os.getenv('DNS_NAMESERVER_1_IP')
    DNS_NAMESERVER_2 = os.getenv('DNS_NAMESERVER_2')
    DNS_NAMESERVER_2_IP = os.getenv('DNS_NAMESERVER_2_IP')
    DNS_NAMESERVER_3 = os.getenv('DNS_NAMESERVER_3')
    DNS_NAMESERVER_3_IP = os.getenv('DNS_NAMESERVER_3_IP')
    DNS_NAMESERVER_4 = os.getenv('DNS_NAMESERVER_4')
    DNS_NAMESERVER_4_IP = os.getenv('DNS_NAMESERVER_4_IP')    

    nameservers = [
        (DNS_NAMESERVER_1,DNS_NAMESERVER_1_IP),
        (DNS_NAMESERVER_2,DNS_NAMESERVER_2_IP),
        (DNS_NAMESERVER_3,DNS_NAMESERVER_3_IP),
        (DNS_NAMESERVER_4,DNS_NAMESERVER_4_IP),        
    ]

class Config_Redis():
    redis_url = os.getenv('REDIS_URL')
    redis_port = os.getenv('REDIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')    

class Config_Presentation():
    presentation_port = int(os.getenv('PRESENTATION_PORT'))
    presentation_interface = os.getenv('PRESENTATION_INTERFACE')
    device_id = os.getenv('DEVICE_ID')

    weight_loss = float(os.getenv('weight_loss'))
    weight_latency = float(os.getenv('weight_latency'))
    weight_jitter = float(os.getenv('weight_jitter'))
    weight_dns_latency = float(os.getenv('weight_dns_latency'))

    threshold_loss = int(os.getenv('threshold_loss'))
    threshold_latency = int(os.getenv('threshold_latency'))
    threshold_jitter = int(os.getenv('threshold_jitter'))
    threshold_dns_latency = int(os.getenv('threshold_dns_latency'))    