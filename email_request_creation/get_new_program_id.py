#input variables to Zapier Code Transfer Step 9: Get New Program ID.
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import re
import datetime

dates = datetime.datetime.today().strftime('%Y-%m-%d').split('-')
name = input['name']

prog_name = 'Email_' + dates[0] + '_' + dates[1] + '_' + dates[2] + '_' + name

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+prog_name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)
pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
return {'pid': pid}
