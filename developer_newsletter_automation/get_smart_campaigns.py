#input variables to Developer Newsletter Creation Step 13: Get Smart Campaigns
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import requests
import re

authorization = "Bearer " + input['token']

url = "https://028-jjw-728.mktorest.com//rest/asset/v1/smartCampaigns.json?folder={\"id\":"+ input['program_id']+", \"type\": \"Program\"}"

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)
smart_campaigns = re.findall('"id":(\d*),"name":',response.text )
print(response.text)
return {'sc_ids':smart_campaigns}
