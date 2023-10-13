#input variables to Zapier  Code Transfer Step 10: Create Marketo Email
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests
import datetime
import urllib.parse
import re
import ast

templates = {"Nurture Series 01" : "1662","Nurture Series 02" : "1671","Nurture Series 03" : "1675","Nurture Series 04" : "1689","Nurture Series 05" : "1697","Nurture Series 06" : "1698","Nurture Series 07" : "1699","Nurture Series 08" : "1700","Nurture Series 09" : "1650", "Transactional" : "1991"}

dictionary = ast.literal_eval(input['dict'])

print(templates[input['template']])

jibberish = ["—", "’"]
char = ["--", "'"]

#print('Before: ', input['value'])
for i in range(0, len(jibberish)):
    dictionary['Subject Line A']=dictionary['Subject Line A'].replace(jibberish[i], char[i])

email_name = "Email " + dictionary['Email Name']

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/emails.json"
authorization = "Bearer " + input['token']

payload = 'folder={"id":' + input['folder_id'] +',"type":'+input['folder_type'] + '}&template=' + templates[input['template']] + '&subject=' + dictionary['Subject Line A'] + '&fromName=' + dictionary['From'] + '&fromEmail=' + dictionary['From Address'] + '&replyEmail=' + dictionary['Reply Address'] + '&operational=' + input['operational'] + '&name=' + email_name

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': authorization
}


response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
eid = re.search('\[{"id":(\d*),', response.text ).group(1)
return {'email_id': eid}
