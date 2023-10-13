#input variables to Zapier Step 10: Update Email Variables
input={
  'variable_names': 'src-Feature*linkButton-FtButton*linkButton-FtButton*textButton-FtButton*title-FeatureBlock*text-FeatureBlock*cardLink*cardSource*cardTitle*cardText*cardLink*cardSource*cardTitle*cardText*cardLink*cardSource*cardTitle*cardText*utm'
  'module_ids': 'featureImgM*featureImgM*featureBlock*featureBlock*featureBlock*featureBlock*card1*card1*card1*card1*card2*card2*card2*card2*card3*card3*card3*card3*'
  'values': 'Variable Values' #from Step 1: New Spreadsheet Row
  'email_id': 'Eid' #from Step 7: Create Email
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'mkto_links': 'Mtko Urls' #from Step 9: Upload Images to Marketo
  }

import urllib.parse

authorization = "Bearer " + input['token']
response=""

replace = ['mkto_link1','mkto_link2','mkto_link3','mkto_link4']
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


headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': authorization
    }
    
for i in range(0, len(variable_names)):
    variable_name = variable_names[i]
    value = urllib.parse.quote(values[i])
    module_id = module_ids[i]
    
    url = "https://028-jjw-728.mktorest.com/rest/asset/v1/email/"+input['email_id']+"/variable/"+variable_name+".json"
    
    if module_id:
         payload = 'value='+value +'&moduleId=' + module_id
    else: #if it is a global variable and does not need a module id e.g. utm
         payload = 'value=' + value
    
    response=response+requests.request("POST", url, headers=headers, data = payload).text+"\n"

return {'response': response}
