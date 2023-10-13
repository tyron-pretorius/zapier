
#input variables to Zapier Step 11: Update Marketo Program Tokens
input={
  'program_id': 'Pid' #from Step 9: Get Latest Marketo Program ID
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'link': 'File URL' #from Step 4: Upload File to Marketo
  'utm': 'Querystring' #from Step 10: Get UTM Parameters from Google Sheet
  'type': 'Content Type' #from Step 1: Get Submission from Google Form
  }


import re
import urllib.parse

authorization = "Bearer " + input['token']

https://developers.marketo.com/rest-api/assets/tokens/#create_and_update
url = "https://###-xxx-###.mktorest.com/rest/asset/v1/folder/" + input['program_id'] + "/tokens.json"

token_type = 'text'
folder_type= 'Program'
token_names= ['utm', 'content link', 'email_utm', 'lead_source','lead_source_detail', 'source','medium','campaign']


content_link = urllib.parse.quote(input['link'])
email_utm = urllib.parse.quote('?utm_source=mkto&utm_medium=email&utm_campaign=content_delivery')
lead_source = 'Content'
lead_source_detail = input['type']

utm = input['utm'].replace("?",'')
source = re.search('utm_source=(.*)&utm_medium',utm).group(1)
medium = re.search('utm_medium=(.*)&utm_campaign',utm).group(1)
campaign = re.search('utm_campaign=(.*)',utm).group(1)   
utm = urllib.parse.quote(utm)
                   
token_values = [utm, content_link, email_utm, lead_source,lead_source_detail, source,medium,campaign]
                
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
