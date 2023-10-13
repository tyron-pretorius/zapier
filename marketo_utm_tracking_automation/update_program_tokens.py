
#input variables to Zapier Step 10: Update Program Tokens
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'program_id': 'pid', #from Step 9: Get New Program ID
  'utm': 'Querystring',#from Step 3: Update Next Row In UTM Builder Sheet
  'lead_source': 'Channel',#from Step 3: Update Next Row In UTM Builder Sheet
  'lead_source_detail': 'Sub-Channel' #from Step 3: Update Next Row In UTM Builder Sheet
  }

import re
import urllib.parse

authorization = "Bearer " + input['token']
url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/" + input['program_id'] + "/tokens.json"

utm=input['utm']
token_type = 'text'
folder_type= 'Program'
token_names= ['utm', 'source', 'medium', 'campaign', 'lead_source', 'lead_source_detail']
source = re.search('utm_source=(.*)&', utm).group(1)
medium = re.search('utm_medium=(.*)&', utm).group(1)
campaign = re.search('utm_campaign=(.*)', utm).group(1)

utm = urllib.parse.quote(utm)
token_values = [utm, source, medium, campaign, input['lead_source'], input['lead_source_detail']]

print (token_values)
                
headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Authorization': authorization
        }
                
response = ''
for i in range(0, len(token_names)):
    payload = 'name=' + token_names[i] + '&value=' + token_values[i] + '&type=' + token_type + '&folderType=' + folder_type
    response = response + requests.request("POST", url, data=payload, headers=headers).text

return {'response': response}
