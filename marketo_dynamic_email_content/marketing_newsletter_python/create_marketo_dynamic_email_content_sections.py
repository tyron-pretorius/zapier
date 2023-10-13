#input variables to Zapier Step 11: Create Marketo Dynamic Email Content Sections
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'modules': 'articleText*articleTextTwo'
  'eid': 'Eid' #from Step 7: Create Email
}

import requests
import re

payload = 'type=DynamicContent&value=1001'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Bearer ' + input['token']
}

modules = input['modules'].split("*")

response = ''

for module in modules:
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/email/'+input['eid']+'/content/'+module+'.json'

    response = response + requests.request("POST", url, headers=headers, data = payload).text

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/email/'+input['eid']+'/content.json'

content_response = requests.request("GET", url, headers={'Authorization': 'Bearer ' + input['token']}, data = {}).text

dynamic_ids = re.findall('"htmlId":"articleText\w*","value":"(.*?)","contentType":', content_response)
                         
return {'dynamic IDs': dynamic_ids, 'content_response':content_response, 'create_response': response}
