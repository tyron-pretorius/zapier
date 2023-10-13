#input variables to Organic Social Campaign Creation Step 11: Schedule Anonymous Campaign
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'parent id': 'fid', #from Step 3: Get Latest Program Ids
  }

import re
import urllib.parse
import calendar
import datetime

response =""
sc_ids = input['sc_ids'].split(",")
sc_names = input['sc_names'].split(",")

for i in range(0,len(sc_ids)):
        if "Anonymous" in sc_names[i]:
            
            url = 'https://028-jjw-728.mktorest.com/rest/v1/campaigns/'+sc_ids[i]+'/schedule.json'
            now = datetime.datetime.now()
            day = str(calendar.monthrange(now.year,now.month)[1])
            month = str(now.month)
            if len(month)<2:
                month = '0' + month
            year = str(now.year)
            date = "-".join([year,month,day])
            payload = '{"input":{"runAt": "'+date+'T23:00:00-05:00"}}'
            headers = {'Content-Type': 'application/json','Authorization': 'Bearer' + input['token']}
                
            response = response + requests.request("POST", url, headers=headers, data =payload).text    

return {'Response': response}
