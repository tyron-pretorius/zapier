#input variables to Monthly Attribution Campaign Cloning Step 9: Get New Program ID
input={
  'token': 'Token', #from Step 3: Get Token
  'year': 'Year', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'month': 'Month', #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  'clone': 'Clone' #from Step 4: Get Lv2 Folder or Create Lv2 Folder
  }

import re

base = re.search('\d*Q\d[\s\-\s]*(.*)', input['clone']).group(1)
q_mapping = {'01':'Q1', '04':'Q2','07':'Q3','10':'Q4'}
name = input['year'] + q_mapping[input['month']] + ' - ' + base

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)
pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
return {'program_id': pid, 'program_name':name, 'base':base}
