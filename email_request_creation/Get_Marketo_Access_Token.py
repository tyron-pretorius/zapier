#input variables to Zapier Code Transfer Step 8: Zapier code transfer
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests
import re
response = requests.get('https://xxx-xxx-xxx.mktorest.com/identity/oauth/token?grant_type=client_credentials&client_id=xxx&client_secret=xxx')

token = re.search('access_token":"(.*)","token_type"', response.text).group(1)

return {'token': token}
