#input variables to Zapier Code Transfer Step 16: Get Smart Campaigns
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests

authorization = "Bearer " + input['token']

url = "https://028-jjw-728.mktorest.com//rest/asset/v1/smartCampaigns.json?folder={\"id\":"+ input['program_id']+", \"type\": \"Program\"}"

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)

return {'id': 1234, 'rawHTML': response.text}
