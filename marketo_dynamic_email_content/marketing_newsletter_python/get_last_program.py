#input variables to Zapier Step 4: Get Last Month's Program by Name
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  }
  
import requests
import datetime
import re
 
now = datetime.datetime.now()
first = now.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)

month = now.month-1 #need to get program from previous month

if month == 0:
    month=12
    year = str(now.year-1) #for Jan of a new year the previous month is in last year
else: 
    year = str(now.year)

month = str(month)    
if len(month)==1:
    month= "0"+month

name = 'Email_' + year + '_'+ month + '_' + lastMonth.strftime("%B") + '_Newsletter'

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)
pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
return {'pid': pid}
