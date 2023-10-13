#input variables to Monthly Attribution Campaign Cloning Step 6: Get Lv4 Folder or Create Lv4 Folder
input={
  'token': 'Token', #from Step 3: Get Token
  'lvl1_info': 'Lv1 Info', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'lvl3_id': 'Lv3 ID', #from Step 5: Get Lv3 Folder or Create Lv3 Folder
  'month': 'Month', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
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

lvl1_info = input['lvl1_info'].split(',')

q_mapping = {'01':'Q1', '04':'Q2','07':'Q3','10':'Q4'}

name = input['year'] +'-' + q_mapping[input['month']] + ' ' + lvl1_info[1]

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + name

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + input['token']
    }

    folder = '{"id":'+input['lvl3_id']+',"type":"Folder"}'

    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)

    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

lvl4_ids = re.findall('"folderId":{"id":(\d*),', response.text)

return {'lv4 id' : lvl4_ids}
