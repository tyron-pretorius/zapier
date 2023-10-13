#input variables to Developer Newsletter Creation Step 5: Clone Last Month's Program
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import urllib.parse
import re

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
    month = "0" + month
    
name = 'Email_' + year + '_' + month + '_' + now.strftime("%B") + '_Developer_Newsletter'

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/'+input['id']+'/clone.json?'

folder = '{"id":' + input["folder_id"] + ',"type":"Folder"}'
    
payload = 'name=' + urllib.parse.quote(name) + '&folder=' + urllib.parse.quote(folder) +  '&description=' + urllib.parse.quote(input['description'])
headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response = requests.request("POST", url, headers=headers, data = payload)
print(response.text)
pid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'pid': pid}
