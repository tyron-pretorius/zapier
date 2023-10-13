#input variables to Developer Newsletter Creation Step 3: Get Parent ID or Create Parent Folder
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import re
import urllib.parse

now = datetime.datetime.now()
year = str(now.year)

name = 'Developer Newsletter ' + year

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer' + input['token']
    }
    
    folder = '{"id":3168,"type":"Folder"}' #"Developer Newsletters" folder
    
    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)
    
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'
    
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text)

ids = re.findall('"folderId":{"id":(\d*),', response.text )

return {'fid': ids}
