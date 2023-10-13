
#input variables to Zapier Step 8: Clone Latest Marketo Program For Sub-Channel
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'program_id': 'pid', #from Step 9: Get New Program ID
  }

import requests
import re

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaigns.json?folder={"id":' + input["program_id"] + ',"type":"Program"}'

response = requests.request("GET", url, headers=headers, data = payload).text
print(response)

sc_ids = re.findall('{"id":(\d*),"name":', response )

return {'sc_ids': sc_ids}
