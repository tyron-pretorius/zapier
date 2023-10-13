#input variables to Zapier Code Transfer Step 8: Clone Last Email Program
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
}

import requests
import datetime
import urllib.parse
import re

dates = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
name = input['name']

prog_name = 'Email_' + dates[0] + '_' + dates[1] + '_' + dates[2] + '_' + name

utm = 'utm_source=mkto&utm_medium=email&utm_campaign='+name.replace(" ","_").lower()

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/'+input['id']+'/clone.json?'

folder = '{"id":' + input["folder_id"] + ',"type":"Folder"}'
    
payload = 'name=' + urllib.parse.quote(prog_name) + '&folder=' + urllib.parse.quote(folder) +  '&description=' + urllib.parse.quote(utm)
headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response = requests.request("POST", url, headers=headers, data = payload)
print(response.text)
pid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'pid': pid}
