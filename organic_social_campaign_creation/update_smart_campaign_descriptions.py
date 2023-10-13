#Step 10: Update Smart Campaign Descriptions
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'sc_ids': 'Sc Ids' #from Step 9: Get Smart Campaign Ids
  }

import requests
import re
import datetime
import urllib.parse

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
    month= "0"+month
    
mediums = ["facebook_organic", "linkedin_organic", "twitter_organic"]
ids=input['sc_ids'].split(",")

response=""

for i in range(0,len(mediums)):
    description = "utm_source=organic_social&utm_medium=" + mediums[i] +"&utm_campaign=rc_"+year+"_"+month
    
    for j in range((4*i),(1+i)*4):
        url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/smartCampaign/'+ids[j]+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    
        
return {'response': response}
