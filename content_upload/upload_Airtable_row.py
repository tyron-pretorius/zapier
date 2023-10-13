#input variables to Zapier Step 6: Upload Row to Airtable
input={
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'rebrandly': 'Rebrandly URL' #from Step 5: Get Rebrandly Link
  'c_name': 'Content Name' #from Step 1: Get Submission from Google Form
  }

import requests
import datetime
import json


#https://airtable.com/api
content_type = {"Case Study": ["recjkV3BC4G1ivVND","Case%20Studies"] , "eBook":["recjAroCT0KNRuHC2","eBooks"], "Fact Sheet":["recRq8P5MHkeK6ZDV","Fact%20Sheets"], "Infographic":["reckG4aGBdkqtYB2z", "Infographics"], "Guide":["recmNFMoRiuE7IF2j", "Other"], "Whitepaper":["recxrhA9kyyGDRES7","Other"]}

c_type = input['c_type']
post_url = "https://api.airtable.com/v0/xxx/"+content_type[c_type][1]
rebrandly= 'https://'+input['rebrandly']
c_name = input['c_name']

headers = {
  'Authorization': 'Bearer xxx',
  'Content-Type': 'application/json'
}

payload ={
  "fields": {
    "Content Name": "["+c_type+"] "+c_name,
    "URL": rebrandly,
    "Content Type": [
      content_type[c_type][0]
    ],
    "Last Updated": datetime.datetime.now().strftime("%Y-%m-%d")
  }
}

response = requests.request("POST", post_url, headers=headers, data = json.dumps(payload))

return {'airtable_response': response.text}
