#input variables to Monthly Attribution Campaign Cloning Step 4: Get Lv2 Folder or Create Lv2 Folder
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

folder_mapping = {'Organic Referral': ['Organic Referral Campaign Tracking','ORCT','3412' ],'Organic Search': ['Organic Search Campaign Tracking','OSeCT', '3387'], 'Organic Social': ['Organic Social Campaign Tracking','OSoCT', '3339'], 'Paid Search': ['Paid Evergreen Campaign Tracking','PECT', '2012'], 'Digital Advertising': ['Paid Evergreen Campaign Tracking','PECT','2012'] , 'Inbound':['Web', 'Web', '1173'], 'Content':['Web', 'Web', '1173']}

match = clone[i].split(" - ")[1]
parent_folder = folder_mapping[match]

payload = {}
headers = {
    'Authorization': 'Bearer ' + input['token']
}


now = datetime.datetime.now()
year = str(now.year)
month = str(now.month)
if len(month)<2:
    month = '0' + month

name = year + ' ' + parent_folder[1]

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name=" + name

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + input['token']
    }

    folder = '{"id":'+parent_folder[2]+',"type":"Folder"}'

    payload = 'name=' + urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)

    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/folders.json'

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

lvl2_ids = re.findall('"folderId":{"id":(\d*),', response.text)

i = i +1
more = False
if i < len(clone):
    more = True

return {'lvl2 id' : lvl2_ids, 'lv1 info':parent_folder, 'clone':program, 'year':year , 'month':month, 'index':i, 'more':more}
