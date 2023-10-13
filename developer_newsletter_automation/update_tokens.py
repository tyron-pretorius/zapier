#input variables to Developer Newsletter Creation Step 7: Update Tokens
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import re
import urllib.parse
import datetime

now = datetime.datetime.now()
year = str(now.year) 

authorization = "Bearer " + input['token']
url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/" + input['program_id'] + "/tokens.json"

#utm = "utm_source=mkto&utm_medium=email&utm_campaign="+now.strftime("%B")+"_developer_newsletter_"+year
token_type = 'text'
folder_type= 'Program'

utm = urllib.parse.quote(input['utm'])
                
headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Authorization': authorization
        }
               
payload = 'name=utm&value=' + utm + '&type=' + token_type + '&folderType=' + folder_type
response = requests.request("POST", url, data=payload, headers=headers).text

return {'response': response}
