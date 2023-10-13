#input variables to Zapier Step 7: Create Email
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'folder_id': 'Pid' #from Step 6: Get New Program ID
  'folder_type': 'Program'
  'template_id': '####'
  'subject': 'Subject Line' #from Step 1: New Spreadsheet Row
  'from_name': 'Team Telnyx',
  'from_add': 'discover@telnyx.com',
  'reply_add': 'discover@telnyx.com',
  'operational': 'False'
  }

import requests
import datetime
import urllib.parse
import re

jibberish = ["—", "’"]
char = ["--", "'"]

#print('Before: ', input['value'])
for i in range(0, len(jibberish)):
    input['subject']=input['subject'].replace(jibberish[i], char[i])

now = datetime.datetime.now()
year = str(now.year) 

email_name = "EM - " + now.strftime("%B") + " " + year

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/emails.json"
authorization = "Bearer " + input['token']

payload = 'folder={"id":' + input['folder_id'] +',"type":'+input['folder_type'] + '}&template=' + input['template_id'] + '&subject=' + input['subject'] + '&fromName=' + input['from_name'] + '&fromEmail=' + input['from_add'] + '&replyEmail=' + input['reply_add'] + '&operational=' + input['operational'] + '&name=' + email_name

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': authorization
}


response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
eid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'eid': eid}
