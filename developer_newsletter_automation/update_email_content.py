#input variables to Developer Newsletter Creation Step 9: Update Email Content
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import requests
import urllib.parse


jibberish = ["—", "’"]
char = ["--", "'"]

#print('Before: ', input['value'])
for i in range(0, len(jibberish)):
    input['value']=input['value'].replace(jibberish[i], char[i])
            
#print("After: Test", input['value'])

encoded = urllib.parse.quote(input['value'])

url='https://028-jjw-728.mktorest.com/rest/asset/v1/email/'+input['email_id']+'/content/'+input['html_id']+'.json'
print(input['value'])
authorization = "Bearer " + input['token']
payload = 'type=' + input['type'] + '&value='+ encoded
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': authorization
}

response = requests.request("POST", url, headers=headers, data=payload)

return {'response': response.text}
