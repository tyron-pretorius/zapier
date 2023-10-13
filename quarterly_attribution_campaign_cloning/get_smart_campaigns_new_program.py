#input variables to Monthly Attribution Campaign Cloning Step 10: Get Smart Campaigns New Program
input={
  'token': 'Token', #from Step 3: Get Token
  'program_id': 'Program ID' #from Step 9: Get New Program ID
  }

import requests
import re

authorization = "Bearer " + input['token']

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaigns.json?folder={\"id\":"+ input['program_id']+", \"type\": \"Program\"}"

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)

sc_ids = re.findall('"id":(\d*),"name":".*?","description":',response.text)
sc_names = re.findall('"id":\d*,"name":"(.*?)","description":',response.text)

return {'sc_ids':sc_ids , 'sc_names': sc_names}
