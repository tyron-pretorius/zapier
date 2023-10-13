#input variables to Zapier Code Transfer Step 6: Get Last Email Program ID
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import re
 
url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json?root={"id":'+input['root']+',"type":"Folder"}'

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)

ids = re.findall('"folderId":{"id":(\d*),"type":"Program"}', response.text )
#not necessary to sort since the API call returns the lastest program last
print(ids)

return {'pid': ids[-1]}
