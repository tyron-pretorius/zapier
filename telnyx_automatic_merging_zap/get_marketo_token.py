#input variables to Zapier Step 2: Get Marketo Access Token
input={
  'base_url': 'https://###-xxx-###.mktorest.com',
  'client_id': 'xxx',
  'client_secret' : 'xxx'
  }

import requests
import re

url = input['base_url'] + '/identity/oauth/token?grant_type=client_credentials&client_id='+ input['client_id'] +'&client_secret='+ input['client_secret']

response = requests.get(url)

token = re.search('access_token":"(.*)","token_type"', response.text).group(1)

return {'token': token}
