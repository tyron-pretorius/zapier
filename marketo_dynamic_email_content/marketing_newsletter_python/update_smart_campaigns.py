#input variables to Zapier Step 14: Update Smart Campaign Descriptions
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'response': 'Response' #from Step 13: Get Smart Campaign IDs
  'values': 'Variable Values' #from Step 1: New Spreadsheet Row
  }

import re
import urllib.parse

search_string= '"id":(\d*),"name":'
smart_campaigns = re.findall(search_string,input['response'] )
#print(smart_campaigns)

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response =""
description = input["values"].split('*')[-1][1:] #the [1:] is just to get rid of the ? at the start of the querystring
for sc_id in smart_campaigns:
        url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_id+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    

return {'response': response}
