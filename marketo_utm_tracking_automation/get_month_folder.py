#input variables to Zapier Step 6: Get or Create Month Folder
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent_id': 'Fid', #from Step 5: Get or Create Year Folder
  }

import requests
import datetime
import urllib.parse
import re

today = str(datetime.datetime.today())

mmmmyy = re.search('(\d*-\d*)',today )
folder = mmmmyy.group(1) + " Campaigns"

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + folder

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)

if 'No assets found for the given search criteria' in response.text:
    parent= '{"id":'+input["parent_id"]+',"type":"Folder"}'

    url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json"

    payload = 'parent=' + parent + '&name=' + urllib.parse.quote(folder)
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
       'Authorization': "Bearer " + input['token']
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    

fid = re.findall('"folderId":{"id":(\d*),', response.text)
return {'fid' : fid}
