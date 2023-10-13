#input variables to Zapier Step 6: Update Winning Lead
input={
  'token': 'xxxx', #from Step 2: Get Marketo Access Token
  'base_url': 'https://###-xxx-###.mktorest.com',
  'final_dict': 'final_dict_string' #from Step 4: Select Winning Field Values
  'field_dict': 'field_dict_string' #from Step 4: Select Winning Field Values
  }

import requests
import json
import ast

#---------------- Update Function Start ------------

#use the Marketo REST API leads endpoint to update a lead field's with the values contained within the input lead_dict
#https://developers.marketo.com/rest-api/lead-database/leads/#create_and_update
def createUpdateLead(base_url, token, lead_dict):

    url = base_url + '/rest/v1/leads.json'

    payload = {
   "action":"updateOnly",
   "lookupField":"id",
   "input": lead_dict
}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return (response.text)

#---------------- Update Function End --------------
field_dict = ast.literal_eval(input['field_dict'])
final_dict = ast.literal_eval(input['final_dict'])

loser_ids = field_dict['id']
loser_ids.remove(final_dict['id'])

update_leads = ['']
update_leads[0] = final_dict

response = createUpdateLead(input['base_url'], input['token'], update_leads)
log = "Update Response:\n" + response + "\n\n"

n = 0

#In the case that Marketo's merging rules selected a different winner than our logic, the the previous update call will contain "skipped" and we then need to cycle through the "loser" ids to find and update the actual winner
while '"status":"skipped"' in str(response) and n < len(loser_ids):
    update_leads[0]['id'] = loser_ids[n]
    log = log + str(update_leads[0]) + "\n\n"
    response = createUpdateLead(input['base_url'], input['token'], update_leads)
    log = log + "Update Response:\n" + response + "\n\n"
    n=n+1
 
return {'log':log}
