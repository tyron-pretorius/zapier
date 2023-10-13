#input variables to Zapier Step 9: Clone Latest Marketo Program
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'pid': 'Program ID' #from Step 8: Get Latest Marketo Program ID
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'c_name': 'Content Name' #from Step 1: Get Submission from Google Form
  'f_info': 'Folder Info' #from Step 7: Get Marketo Folder ID
  'description': 'File URL' #from Step 4: Upload File to Marketo
  }
  
  
import requests
import re
import datetime
import urllib.parse
import json

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
    month = "0" + month

c_type =input['c_type']
c_name =input['c_name']
f_info = input['f_info']
fid = f_info.split(":")[1]
print (now.year, now.month)

#https://developers.marketo.com/rest-api/assets/programs/#clone
url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/program/'+input['pid']+'/clone.json?'


name =  "Content_" + c_type + "_" + year + "_" + month + "_" + c_name 
folder = '{"id":' + fid + ',"type":"Folder"}'

payload = 'name=' + urllib.parse.quote(name) + '&folder=' + urllib.parse.quote(folder) +  '&description=' + urllib.parse.quote(input['description'])
headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response = requests.request("POST", url, headers=headers, data = payload)
result = re.search('"result":\[(.*)\]}', response.text).group(1)
load = json.loads(result)

return {'pid': load["id"], 'name':load["name"], 'url':load["url"]}
