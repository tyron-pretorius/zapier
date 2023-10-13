import requests
import re
response = requests.get('https://###-xxx-###.mktorest.com/identity/oauth/token?grant_type=client_credentials&client_id=xxx&client_secret=xxx')

token = re.search('access_token":"(.*)","token_type"', response.text).group(1)

return {'token': token}
