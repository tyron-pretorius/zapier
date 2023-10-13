#input variables to Developer Newsletter Creation Step 8: Create Email
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import re

now = datetime.datetime.now()
year = str(now.year) 

email_name = "EM - " + now.strftime("%B") + " Dev " + year

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/emails.json"
authorization = "Bearer " + input['token']

payload = 'folder={"id":' + input['program_id'] +',"type":'+input['folder_type'] + '}&template=' + input['template_id'] + '&subject=' + input['subject'] + '&fromName=' + input['from_name'] + '&fromEmail=' + input['from_add'] + '&replyEmail=' + input['reply_add'] + '&operational=' + input['operational'] + '&name=' + email_name

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': authorization
}


response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
eid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'eid': eid}
