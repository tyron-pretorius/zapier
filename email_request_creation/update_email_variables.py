#input variables to Zapier Code Transfer Step 13: Update Email Variables
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import urllib.parse
import ast

authorization = "Bearer " + input['token']
response=""

headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': authorization
    }

mapping = ast.literal_eval(input['dict'])

mapping['UTM']='?utm_source=mkto&utm_medium=email&utm_campaign='+mapping['Email Name'].replace(" ","_").lower()

print(mapping)
if 'Button Link' in mapping and mapping['Button Link']!='':
    mapping['Banner Source'] = mapping['Button Link']
print(mapping)

remove = ['Email Name', 'From', 'From Address', 'Reply Address', 'Subject Line A', 'Subject Line B','Preheader Text', 'Template']

for r in remove:
    mapping.pop(r, None)

mkto_ids =  {'Banner Image (600x300px @1x | 1200x600px @2x)': ['img-Hero', 'hero'], 'Banner Source': ['link-Hero', 'hero'] , 'Main Title': ['text-Title', 'title'],'Pre-Button Text': ['', 'bodyTextBlock'],'Button Text': ['textButton-Button', 'button'],'Button Link': ['linkButton-Button', 'button'],'Post-Button Text': ['', 'bodyTextBlock2'], 'UTM':['UTM','']}

jibberish = ['—', '’']
char = ['--', '\'']

for key, val in mapping.items():
    variable_name = mkto_ids[key][0]
    if variable_name: #if it is not the empty string i.e. keys we do not want to update
        module_id = mkto_ids[key][1]
        value = urllib.parse.quote(val)

        for i in range(0, len(jibberish)):
            value=value.replace(jibberish[i], char[i])

        url = "https://028-jjw-728.mktorest.com/rest/asset/v1/email/"+input['email_id']+"/variable/"+variable_name+".json"
        if module_id:
             payload = 'value='+value +'&moduleId=' + module_id
        else: #if it is a global variable and does not need a module id e.g. utm
             payload = 'value=' + value

        response=response+requests.request("POST", url, headers=headers, data = payload).text+"\n"

return {'response': response, 'dict': str(mapping)}
