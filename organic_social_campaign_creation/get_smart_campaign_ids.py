#Step 9: Get Smart Campaign Ids
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'fb_pid': 'Pid', #from Step 5: Clone Facebook Program
  'li_pid': 'Pid', #from Step 6: Clone LinkedIn Program
  'tw_pid': 'Pid' #from Step 7: Clone Twitter Program
  }

import requests
import re

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

response=""

ids = [input["fb_pid"],input["li_pid"],input["tw_pid"]]

for i in ids:
    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaigns.json?folder={"id":' + i + ',"type":"Program"}'
    response = response + requests.request("GET", url, headers=headers, data = payload).text

sc_ids = re.findall('"id":(\d*),"name":".*?","description":',response)
sc_names = re.findall('"id":\d*,"name":"(.*?)","description":',response)

print(response)
return {'sc_ids':sc_ids , 'sc_names': sc_names}
