#input variables to Zapier Code Transfer Step 5: Get Parent ID or Creat Parent Folder
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import re
import urllib.parse

now = datetime.datetime.now()
year = str(now.year) 

name = year + " Mass Mailers"

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
    
    folder = '{"id":43,"type":"Folder"}' #"Mass Mailers" folder
    
    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)
    
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'
    
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text)

fid = re.findall('"folderId":{"id":(\d*),', response.text )

return {'fid': fid}
