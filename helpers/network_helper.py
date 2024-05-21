# Network tests
import subprocess
import json
from threading import Thread
import dns.resolver
import speedtest


class NetworkCollector(object): # Main network collection class

    def __init__(self,sites,count,dns_test_site,nameservers_external):
        self.sites = sites # List of sites to ping
        self.count = str(count) # Number of pings
        self.stats = [] # List of stat dicts
        self.dnsstats = [] # List of stat dicts
        self.dns_test_site = dns_test_site # Site used to test DNS response times
        self.nameservers = []
        self.nameservers = nameservers_external


    def pingtest(self,count,site):

        ping = subprocess.getoutput(f"ping -n -i 0.1 -c {count} {site} | grep 'rtt\|loss'")

        try:
            loss = ping.split(' ')[5].strip('%')
            latency=ping.split('/')[4]
            jitter=ping.split('/')[6].split(' ')[0]

            netdata = {
                "site":site,
                "latency":latency,
                "loss":loss,
                "jitter":jitter
            }

            self.stats.append(netdata)

        except:
            print(f"Error pinging {site}")
            return False

        return True

    def dnstest(self,site,nameserver):
        
        my_resolver = dns.resolver.Resolver()

        server = [] # Resolver needs a list
        server.append(nameserver[1])


        try:

            my_resolver.nameservers = server
            my_resolver.timeout = 10

            answers = my_resolver.query(site,'A')

            dns_latency = round(answers.response.time * 1000,2)

            dnsdata = {
                "nameserver":nameserver[0],
                "nameserver_ip":nameserver[1],
                "latency":dns_latency
            }

            self.dnsstats.append(dnsdata)

        except Exception as e:
            print(f"Error performing DNS resolution on {nameserver}")
            print(e)

            dnsdata = {
                "nameserver":nameserver[0],
                "nameserver_ip":nameserver[1],
                "latency":5000
            }
            
            self.dnsstats.append(dnsdata)

        return True

    def collect(self):

        # Empty preveious results
        self.stats = []
        self.dnsstats = []

        # Create threads, start them
        threads = []

        for item in self.sites:
            t = Thread(target=self.pingtest, args=(self.count,item,))
            threads.append(t)
            t.start()

        # Wait for threads to complete
        for t in threads:
            t.join()

        # Create threads, start them
        threads = []            

        for item in self.nameservers:
            s = Thread(target=self.dnstest, args=(self.dns_test_site,item,))
            threads.append(s)
            s.start()            

        # Wait for threads to complete
        for s in threads:
            s.join()

        results = json.dumps({
            "stats":self.stats,
            "dns_stats":self.dnsstats
        })

        return results


class Netprobe_Speedtest(object): # Speed test class

    def __init__(self):
        self.speedtest_stats = {"download": None, "upload": None}

    def netprobe_speedtest(self):

        s = speedtest.Speedtest()
        s.get_best_server()
        download = s.download()
        upload = s.upload()

        self.speedtest_stats = {
            "download": download,
            "upload": upload
        }

    def collect(self):

        self.speedtest_stats = {"download": None, "upload": None}
        self.netprobe_speedtest()

        results = json.dumps({
            "speed_stats":self.speedtest_stats
        })

        return results







