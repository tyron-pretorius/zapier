#input variables to Zapier Step 8: Clone Latest Marketo Program For Sub-Channel
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'id': 'pid', #from Step 7: Get Latest Marketo Program For Sub-Channel
  'folder': 'fid', #from Step 6: Get or Create Month Folder
  'description': 'Querystring',#from Step 3: Update Next Row In UTM Builder Sheet
  'name' : 'Campaign Name', #from Step 1: New UTM Request Form Submission
  'sub-channel':'Sub-Channel' #from Step 3: Update Next Row In UTM Builder Sheet
  }

import requests
import re
import datetime
import urllib.parse

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/program/'+input['id']+'/clone.json?'

sub_channel = input['sub_channel']

mapping = {'Advertising':'Digital Advertising','Paid_Search':'Paid Search',}
channel = mapping[input['channel']]

if len(month)==1:
        month =  "0" + month
        
name =  year + month + " - " + channel + " - " + sub_channel + " - " + re.search('\s([\w*\s]+)', input['name']).group(1)

folder = '{"id":' + input['folder'] + ',"type":"Folder"}'

payload = 'name=' + urllib.parse.quote(name) + '&folder=' + urllib.parse.quote(folder) +  '&description=' + urllib.parse.quote(input['description'])
headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response = requests.request("POST", url, headers=headers, data = payload)
pid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'pid': pid, 'name': name}
