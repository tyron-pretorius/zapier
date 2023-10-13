#Step 6: Clone LinkedIn Program
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'ids': 'Pids', #from Step 3: Get Latest Program Ids
  'folder' : 'Fid', #from Step 4: Get or Create Latest Folder
  }

import requests
import re
import datetime
import urllib.parse

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

folder = '{"id":' + input['folder'] + ',"type":"Folder"}'

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
    month= "0"+month

name = year+month+  " - Organic Social - LinkedIn"
medium = "linkedin_organic"
id=input['ids'].split(",")[1]

description = "utm_source=organic_social&utm_medium=" + medium +"&utm_campaign=rc_"+year+"_"+month

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/'+id+'/clone.json?'

payload = 'name=' + urllib.parse.quote(name) + '&folder=' + urllib.parse.quote(folder) +  '&description=' + urllib.parse.quote(description)

response = requests.request("POST", url, headers=headers, data = payload)
pid = re.findall('{"id":(\d*),', response.text )

return {'pid': pid}
