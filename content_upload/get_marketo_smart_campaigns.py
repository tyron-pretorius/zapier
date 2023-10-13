#input variables to Zapier Step 14: Get Marketo Smart Campaign IDs
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'program_id': 'Pid' #from Step 9: Clone Latest Marketo Program
  }

import requests
import re

authorization = "Bearer " + input['token']

#https://developers.marketo.com/rest-api/assets/smart-campaigns/#browse
url = "https://###-xxx-###.mktorest.com/rest/asset/v1/smartCampaigns.json?folder={\"id\":"+ input['program_id']+", \"type\": \"Program\"}"

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)

search_string= '"id":(\d*),"name":'
sc_ids = re.findall(search_string,response.text)

return {'sc_ids': sc_ids, 'response': response.text}
