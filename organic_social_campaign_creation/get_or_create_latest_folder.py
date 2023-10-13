#Step 4: Get or Create Latest Folder
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  }

import requests
import datetime
import re
import urllib.parse

now = datetime.datetime.now()
year = str(now.year)

folder = year + " OSoCT FB LI TW"

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + folder

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)

if 'No assets found for the given search criteria' in response.text:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + input['token']
    }
    
    parent= '{"id":3339,"type":"Folder"}' #this is for "Organic Social Campaign Tracking" Folder

    payload = 'name=' + urllib.parse.quote(folder) + '&parent=' + urllib.parse.quote(parent)
    
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'

    response = requests.request("POST", url, headers=headers, data=payload)
    
fid = re.search('"folderId":{"id":(\d*),"type":"Folder"}', response.text).group(1)
return {'fid': fid}
