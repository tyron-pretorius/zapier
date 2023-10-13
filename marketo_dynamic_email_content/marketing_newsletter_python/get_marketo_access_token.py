#input variables to Zapier Step 2: Get Marketo Access Token
input={
  'client_id': 'xxx' #https://developers.marketo.com/rest-api/authentication/
  'client_secret': 'xxx' #https://developers.marketo.com/rest-api/authentication/
  'base_url': 'https://###-xxx-###.mktorest.com'
  }

import requests
import re
import time
import json

remaining = 0
wait = 120 #secs

while remaining < wait:
    time.sleep(remaining)

    temp = json.loads(requests.get(
        input['base_url']+'/identity/oauth/token?grant_type=client_credentials&client_id=' +input['client_id'] +'&client_secret='+input['client_secret']).text)

    token = temp['access_token']
    remaining = temp['expires_in']

return { 'token': token, 'remaining': remaining}
