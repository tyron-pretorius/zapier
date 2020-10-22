#input variables to Zapier Step 13: Rename Marketo Email
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'eid': 'Email_id' #from Step 12: Get Marketo Email ID
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'c_name': 'Content Name' #from Step 1: Get Submission from Google Form
  }
  
import requests
import re
import datetime
import urllib.parse

if (input['c_type'] != 'Fact Sheet' and input['c_type'] != 'Infographic'):
    now = datetime.datetime.now()
    year = str(now.year) 
    month = str(now.month)

    if len(month)==1:
        month = "0" + month

    #https://developers.marketo.com/rest-api/assets/emails/#create_and_update
    url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/email/'+input['eid']+'.json'

    name =  "EM - Content_" + input['c_type'] + "_" + year + "_" + month + "_" + input['c_name'] 

    print(name)

    payload = 'name=' + urllib.parse.quote(name)

    headers = {
     'Content-Type': 'application/x-www-form-urlencoded',
     'Authorization': 'Bearer' + input['token']
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    return {'response': response.text}
