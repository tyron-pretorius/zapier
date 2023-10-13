#input variables to Zapier Step 12: Update Smart Campaign Descriptions
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'sc_ids': 'sc_ids', #from Step 11: Get Smart Campaign IDs
  'utm': 'Querystring' #from Step 3: Update Next Row In UTM Builder Sheet
  }

import re
import urllib.parse

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response =""
description = input["utm"]
smart_campaigns=  input["sc_ids"].split(",")

for sc_id in smart_campaigns:
        url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_id+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    
        
return {'response': response}
