#input variables to Zapier Code Transfer Step 17: Update Smart Campaign Descriptions
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import re
import urllib.parse
import ast

mapping = ast.literal_eval(input['dict'])

search_string= '"id":(\d*),"name":'
smart_campaigns = re.findall(search_string,input['raw'] )
#print(smart_campaigns)

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response =""
description = mapping['UTM']
for sc_id in smart_campaigns:
        url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_id+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    

return {'id': 1234, 'rawHTML': response}
