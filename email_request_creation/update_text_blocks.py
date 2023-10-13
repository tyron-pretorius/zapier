#input variables to Zapier Step 14: Update Text Blocks
input={
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'dict': 'Dict' #from Step 13: Get Text Blocks
  'email_id' : 'Email ID' : #from Step 9: Create Marketo Email
  }

import requests
import urllib.parse
import ast

mapping = ast.literal_eval(input['dict'])

mkto_ids =  {'Banner Image (600x300px @1x | 1200x600px @2x)': ['img-Hero', 'hero'], 'Banner Source': ['link-Hero', 'hero'] , 'Main Title': ['text-Title', 'title'],'Pre-Button Text': ['', 'bodyText1'],'Button Text': ['textButton-Button', 'button'],'Button Link': ['linkButton-Button', 'button'],'Post-Button Text': ['', 'bodyText2'], 'UTM':['UTM','']}

text_block_names=[]

for key in mapping:
    if mkto_ids[key][0] =='':
        text_block_names.append(key)

text_block_values = [None]*len(text_block_names)

response = ""

for k in range(0,len(text_block_names)):

    encoded = urllib.parse.quote(mapping[text_block_names[k]])
    
    print(mkto_ids[text_block_names[k]][1])
    
    url='https://028-jjw-728.mktorest.com/rest/asset/v1/email/'+input['email_id']+'/content/'+mkto_ids[text_block_names[k]][1]+'.json'
    
    authorization = "Bearer " + input['token']
    payload = 'type=text&value='+ encoded
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': authorization
    }

    response = response + requests.request("POST", url, headers=headers, data=payload).text

return {'Response': response}
