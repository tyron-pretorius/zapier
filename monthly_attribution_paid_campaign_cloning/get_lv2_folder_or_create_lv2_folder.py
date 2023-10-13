#input variables to Monthly Attribution Paid Campaign Cloning Step 4: Get Lv2 Folder or Create Lv2 Folder
input={
  'token': 'Token', #from Step 3: Get Token
  'clone' : 'Monthly Programs', #from Step 2: Lookup Program Names
  'index': 'Index' #from Step 1: Catch Webhook From Google Script
  }

import requests
import datetime
import re
import urllib.parse

i = int(input['index'])
clone = input['clone'].split('*')
program = clone[i]

payload = {}
headers = {
    'Authorization': 'Bearer ' + input['token']
}

now = datetime.datetime.now()
year = str(now.year)
month = str(now.month)
if len(month)<2:
    month = '0' + month

name = year + ' Paid Campaigns'

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + name

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + input['token']
    }

    folder = '{"id":2154,"type":"Folder"}'

    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)

    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

lvl2_ids = re.findall('"folderId":{"id":(\d*),', response.text)

i = i +1
more = False
print(i)
print(len(clone))
if i < len(clone):
    more = True

return {'lvl2 id' : lvl2_ids, 'clone':program, 'year':year , 'month':month, 'index':i, 'more':more}
