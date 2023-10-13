#input variables to Yearly Attribution Campaign Cloning Step 10: Activate + Schedule Smart Campaigns
input={
  'token': 'Token', #from Step 3: Get Token
  'sc_ids': 'sc_ids', #from Step 9: Get Smart Campaigns New Program
  'sc_names': 'sc_names' #from Step 9: Get Smart Campaigns New Program
  }

import re
import urllib.parse
import calendar
import datetime

response =""
sc_ids = input['sc_ids'].split(",")
sc_names = input['sc_names'].split(",")

for i in range(0,len(sc_ids)):
        if "Anonymous" not in sc_names[i]:
            url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+sc_ids[i]+'/activate.json'
            payload ={}
            headers = {
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'Authorization': 'Bearer' + input['token']
                    }
        else: #schedule the batch program to run one last time before it is deleted by next month's program
            
            url = 'https://028-jjw-728.mktorest.com/rest/v1/campaigns/'+sc_ids[i]+'/schedule.json'
            now = datetime.datetime.now()
            day = str(calendar.monthrange(now.year,now.month+11)[1])
            month = str(now.month+11)
            if len(month)<2:
                month = '0' + month
            year = str(now.year)
            date = "-".join([year,month,day])
            payload = '{"input":{"runAt": "'+date+'T23:00:00-05:00"}}'
            headers = {'Content-Type': 'application/json','Authorization': 'Bearer' + input['token']}
                
        response = response + requests.request("POST", url, headers=headers, data =payload).text    

return {'Response': response}
