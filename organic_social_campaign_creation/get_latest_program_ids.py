#Step 3: Get Latest Program Ids
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  }

import requests
import datetime
import re

now = datetime.datetime.now()
month = now.month-1 #need to get campaigns from previous month

if month == 0:
    month=12
    year = str(now.year-1) #for Jan of a new year the previous month is in last year
else: 
    year = str(now.year)

month = str(month)    
if len(month)==1:
    month= "0"+month
    
name_base = year+month + " - Organic Social - "

name_ends = ["Facebook","LinkedIn","Twitter"]

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

response=""

for i in name_ends:
    url = "https://028-jjw-728.mktorest.com/rest/asset/v1/program/byName.json?name="+name_base+i

    response = response + requests.request("GET", url, headers=headers, data = payload).text

ids = re.findall('{"id":(\d*),', response )

return {'pids': ids}
