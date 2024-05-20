# Redis helper
# 
# Functions to help read and write from Redis


from config import Config_Redis
import redis
import json

class RedisConnect():

    def __init__(self):

        # Load global variables
        
        self.redis_url = Config_Redis.redis_url
        self.redis_port = Config_Redis.redis_port
        self.redis_password = Config_Redis.redis_password

        self.r = redis.Redis( # Connect to Redis
            host=self.redis_url,
            port=self.redis_port
        )

    def redis_read(self,key): # Read data from Redis

        results = self.r.get(key) # Get the latest results from Redis for a given key

        if results:
            data = json.loads(results)
        else:
            data = ""

        return data

    def redis_write(self,key,data,ttl): # Write data to Redis

        write = self.r.set(key,json.dumps(data),ttl) # Store data with a given TTL

        return write
    