#input variables to Monthly Attribution Paid Campaign Cloning Step 6: Get Old Program 
input={
  'token': 'Token', #from Step 3: Get Token
  'name': 'Clone', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  }

import requests
import re
import json

authorization = "Bearer " + input['token']

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/byName.json?name='+input['name']

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)
result = re.search('"result":\[(.*)\]}',response.text).group(1)
description = json.loads(result)['description']
pid = json.loads(result)['id']

if not description: #description is empty
    description = 'empty'

return {'pid':pid, 'description': description}
