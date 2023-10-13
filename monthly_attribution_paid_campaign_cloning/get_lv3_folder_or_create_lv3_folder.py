#input variables to Monthly Attribution Paid Campaign Cloning Step 5: Get Lv3 Folder or Create Lv3 Folder 
input={
  'token': 'Token', #from Step 3: Get Token
  'month': 'month', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'lvl2_id': 'Lvl2 ID', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'year': 'Year' #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  }

import requests
import datetime
import re
import urllib.parse

payload = {}
headers = {
    'Authorization': 'Bearer ' + input['token']
}

name = input['year'] +'-' + input['month'] + ' Campaigns'

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + name

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + input['token']
    }

    folder = '{"id":'+input['lvl2_id']+',"type":"Folder"}'

    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)

    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

lvl3_ids = re.findall('"folderId":{"id":(\d*),', response.text)

return {'lvl3 id' : lvl3_ids}
