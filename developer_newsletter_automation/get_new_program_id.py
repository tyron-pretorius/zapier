#input variables to Developer Newsletter Creation Step 6: Get New Program ID
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import re
import datetime

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
    month = "0" + month
    
name = 'Email_' + year + '_' + month + '_' + now.strftime("%B") + '_Developer_Newsletter'

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text)
pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
return {'pid': pid}
