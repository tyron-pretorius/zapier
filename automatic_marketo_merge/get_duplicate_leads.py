#input variables to Zapier Step 3: Get Duplicate Leads
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'lookup_value': 'Email Address', #from Step 1: Lead Added to Duplicates List
  'lookup_field_api_name': 'email',
  'base_url': 'https://###-xxx-###.mktorest.com',
  'field_names': 'id,sfdcLeadId,email,createdAt,firstName,lastName,leadSource,Lead_Source_Detail__c,unsubscribed, leadStatus'
  }

import requests
import json
import re
import urllib.parse


url = input['base_url'] + '/rest/v1/leads.json?filterType='+input['lookup_field_api_name']+'&filterValues='+input['lookup_value']+'&fields='+input['field_names']
print(input['field_names'])
print(url)
headers = {
  'Authorization': 'Bearer '+input['token']
}

response = requests.request("GET", url, headers=headers)
print(response.text)
result = re.search('"result":\[(.*)\]',response.text).group(1)
people = re.findall('{.*?}',result)

return{'ids':people}
