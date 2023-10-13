#input variables to Developer Newsletter Creation Step 12: Update Email Variables
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import urllib.parse

authorization = "Bearer " + input['token']
response=""

replace = ['mkto_link1','mkto_link2','mkto_link3']
mkto_links = input['mkto_links'].split(",")

print(input['values'])
      
for i in range(0,len(replace)):
    input['values']=input['values'].replace(replace[i], mkto_links[i])

print(input['values'])

jibberish = ["—", "’"]
char = ["--", "'"]

#print('Before: ', input['values'])
for i in range(0, len(jibberish)):
    input['values']=input['values'].replace(jibberish[i], char[i])
            
#print("After: Test", input['values'])

values = input['values'].split("*")
module_ids = input['module_ids'].split("*")
variable_names = input['variable_names'].split("*")

for i in range(0, len(variable_names)):
    variable_name = variable_names[i]
    
    value = urllib.parse.quote(values[i])

    module_id = module_ids[i]
    url = "https://028-jjw-728.mktorest.com/rest/asset/v1/email/"+input['email_id']+"/variable/"+variable_name+".json"
    if module_id:
         payload = 'value='+value +'&moduleId=' + module_id
    else: #if it is a global variable and does not need a module id e.g. utm
         payload = 'value=' + value
    
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': authorization
    }
    response=response+requests.request("POST", url, headers=headers, data = payload).text+"\n"

return {'response': response}
