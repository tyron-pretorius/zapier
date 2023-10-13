#input variables to Zapier Step 15: Update Marketo Smart Campaign Descriptions
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'utm': 'Querystring' #from Step 10: Get UTM Parameters from Google Sheet
  'sc_ids': 'Sc ids' #from Step 14: Get Marketo Smart Campaign IDs
  }
  
  
import re
import urllib.parse

search_string= '"id":(\d*),"name":'
smart_campaigns = input['sc_ids'].split(",")

headers = {
 'Content-Type': 'application/x-www-form-urlencoded',
 'Authorization': 'Bearer' + input['token']
}

response =""
description = input['utm'].replace("?",'')
for sc_id in smart_campaigns:
        #https://developers.marketo.com/rest-api/assets/smart-campaigns/#update
        url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/smartCampaign/'+sc_id+'.json'
        payload = 'description=' + urllib.parse.quote(description)
        response = response + requests.request("POST", url, headers=headers, data = payload).text    

return {'response': response}
