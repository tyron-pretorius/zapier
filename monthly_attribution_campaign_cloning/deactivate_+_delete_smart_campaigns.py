#input variables to Monthly Attribution Campaign Cloning Step 13: Deactivate + Delete Smart Campaigns
input={
  'token': 'Token', #from Step 3: Get Token
  'sc_ids': 'sc_ids', #from Step 12: Get Smart Campaigns Old Program
  'sc_names': 'sc_names' #from Step 12: Get Smart Campaigns Old Program
  }

import re
import urllib.parse
import calendar
import datetime

headers = {
         'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': 'Bearer' + input['token']
        }

response =""
sc_ids = input['sc_ids'].split(",")
sc_names = input['sc_names'].split(",")

for i in range(0,len(sc_ids)):
        if "Anonymous" not in sc_names[i]:
            url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_ids[i]+'/deactivate.json'
            
        else:
            url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_ids[i]+'/delete.json'
                
        response = response + requests.request("POST", url, headers=headers, data ={}).text    

return {'Response': response}
