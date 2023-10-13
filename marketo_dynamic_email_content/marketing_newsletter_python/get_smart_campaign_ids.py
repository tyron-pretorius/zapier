#input variables to Zapier Step 13: Get Smart Campaign IDs
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'program_id': 'Pid' #from Step 6: Get New Program ID
  }

import requests

authorization = "Bearer " + input['token']

url = "https://028-jjw-728.mktorest.com//rest/asset/v1/smartCampaigns.json?folder={\"id\":"+ input['program_id']+", \"type\": \"Program\"}"

payload = {}
headers = {
  'Authorization': authorization
}

response = requests.request("GET", url, headers=headers, data = payload)
#smart_campaigns = re.findall('"id":(\d*),"name":',response.text )
#print(response.text)
#return {'sc_ids':smart_campaigns}
return {'response': response.text}
