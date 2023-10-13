#input variables to Zapier Step 5: Get or Create Year Folder
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  }

import requests
import datetime
import re
import urllib.parse

now = datetime.datetime.now()
year = str(now.year)

name = year + ' Paid Campaigns'

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
    
    folder= '{"id":2154,"type":"Folder"}' #this is for "Paid Campaign Tracking" Folder
    
    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)
    
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'
    
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text)

ids = re.findall('"folderId":{"id":(\d*),', response.text )

return {'fid': ids}
