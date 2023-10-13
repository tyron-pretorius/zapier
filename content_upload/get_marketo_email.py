
#input variables to Zapier Step 12: Get Marketo Email ID
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'pid': 'Pid' #from Step 9: Clone Latest Marketo Program
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  }
  
  
import requests
import datetime
import re

if (input['c_type'] != 'Fact Sheet' and input['c_type'] != 'Infographic'):
    pid = input['pid']

    #https://developers.marketo.com/rest-api/assets/emails/#browse
    url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/emails.json?folder={\"id\":'+pid+',\"type\":\"Program\"}'

    payload = {}
    headers = {
      'Authorization': 'Bearer ' + input['token']
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    raw=response.text

    eid = re.search('{"id":(\d*),',response.text).group(1)
    return {'email_id': eid}
