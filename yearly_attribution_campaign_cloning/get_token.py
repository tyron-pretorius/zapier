import requests
import re
import time
import json

remaining = 0
wait = 60 #secs

while remaining < wait:
    time.sleep(remaining)

    temp = json.loads(requests.get(
        'https://xxx-xxx-xxx.mktorest.com/identity/oauth/token?grant_type=client_credentials&client_id=xxx&client_secret=xxx').text)

    token = temp['access_token']
    remaining = temp['expires_in']

return { 'token': token, 'remaining': remaining}
