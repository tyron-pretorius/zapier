#input variables to Developer Newsletter Creation Step 14: Update Smart Campaign Descriptions
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import re
import urllib.parse

smart_campaigns = input['sc_ids'].split(',')

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response =""
description = input["utm"]
for sc_id in smart_campaigns:
        url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_id+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    

return {'id': 1234, 'rawHTML': response}
