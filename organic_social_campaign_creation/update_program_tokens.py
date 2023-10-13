#Step 8: Update Program Tokens
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'fb_pid': 'Pid', #from Step 5: Clone Facebook Program
  'li_pid': 'Pid', #from Step 6: Clone LinkedIn Program
  'tw_pid': 'Pid' #from Step 7: Clone Twitter Program
  }

import re
import urllib.parse
import datetime

authorization = "Bearer " + input['token']

headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Authorization': authorization
        }

token_type = 'text'
folder_type= 'Program'
token_names= ['utm', 'campaign']
mediums = ["facebook_organic", "linkedin_organic", "twitter_organic"]

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)
if len(month)==1:
    month= "0"+month
campaign= "rc_"+year+"_"+month

ids = [input["fb_pid"],input["li_pid"],input["tw_pid"]]

response = ''

for i in range(0,len(ids)):
    response = response + 'Program '+ str(i) + ": "
    utm = "utm_source=organic_social&utm_medium=" + mediums[i] +"&utm_campaign="+campaign
    utm = urllib.parse.quote(utm)
    token_values = [utm, campaign]

    url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/" + ids[i] + "/tokens.json"

    for j in range(0, len(token_names)):
        payload = 'name=' + token_names[j] + '&value=' + token_values[j] + '&type=' + token_type + '&folderType=' + folder_type
        response = response + requests.request("POST", url, data=payload, headers=headers).text

          
return {'response': response}
