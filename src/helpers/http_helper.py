import requests
import json

class CallHome(object): # Call home http functions

    def __init__(self):
        pass

    def post_stats(self,url,stats):

        headers={"Content-Type":"application/json"}
        
        request = requests.post(url, data=stats,headers=headers)

        return (request.status_code,request.content)
