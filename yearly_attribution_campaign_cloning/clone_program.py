#input variables to Yearly Attribution Campaign Cloning Step 7: Clone Program
input={
  'token': 'Token', #from Step 3: Get Token
  'year': 'Year', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'month': 'Month', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'clone': 'Clone', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'lvl3_id': 'Lv3 ID', #from Step 5: Get Lv3 Folder or Create Lv3 Folder
  'description': 'Description', #from Step 6: Get Old Program
  }

import requests
import datetime
import urllib.parse
import re

response = requests.request("GET", "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+input['clone'], headers={'Authorization': 'Bearer '+input['token']}, data = {})

pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)

base = re.search('\d*[\s\-\s]*(.*)', input['clone']).group(1)

name = input['year'] + ' - ' + base

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/'+pid+'/clone.json?'

folder = '{"id":' + input["lvl3_id"] + ',"type":"Folder"}'


payload = 'name=' + urllib.parse.quote(name) + '&folder=' + urllib.parse.quote(folder)

if input['description'] != 'empty':
    payload = payload + '&description='+urllib.parse.quote(input['description'])

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response = requests.request("POST", url, headers=headers, data = payload)
print(response.text)
pid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'program_id': pid, 'program_name':name, 'base':base}
