#input variables to Zapier Step 5: Merge Leads
input={
  'field_dict': 'field_dict_string', #from Step 4: Select Winning Field Values
  'final_dict': 'final_dict_string', #from Step 4: Select Winning Field Values
  'base_url': 'https://###-xxx-###.mktorest.com',
  'token': 'xxxxxx' #from Step 2: Get Marketo Access Token
  }

import ast
import requests

#------------- Merge Function Start ------------------
#this function merges multiple leads together using the merge REST API endpoint
#https://developers.marketo.com/rest-api/lead-database/leads/#merge
def mergeLead(base_url, token, winner_id, loser_ids, CRMmerge):

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    #When mergeinCRM is TRUE then you can only merge two leads at a time (when this is false you can merge multiple
    #leads in a single call) hence why a for loop is needed to successively merge each of the losing ids with the winner
    loser_ids = [str(x) for x in loser_ids]
    response = []
    for i in loser_ids:
        url = base_url + '/rest/v1/leads/' + str(winner_id) + '/merge.json?mergeInCRM=' + str(CRMmerge) + '&leadIds=' + i
        response.append(requests.request("POST", url, headers=headers, data=payload).text)

    return (response)

#------------- Merge Function End ------------------

field_dict = ast.literal_eval(input['field_dict'])
final_dict = ast.literal_eval(input['final_dict'])

loser_ids = field_dict['id']
loser_ids.remove(final_dict['id'])

response = mergeLead(input['base_url'], input['token'], final_dict['id'], loser_ids, True)

log = "Merge Response:\n" + str(response)+"\n\n"

return{'log':log}
