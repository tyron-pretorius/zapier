#input variables to Zapier Step 4: Upload File to Marketo
input={
  'path': 'Content Link' #from Step 2: Get Dropbox Temporary Link
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'c_name': 'Content Name' #from Step 1: Get Submission from Google Form
  'token' : 'Token' #from Step 3: Get Marketo Access Token
  }


import requests
import urllib
import json
import re

c_type = input['c_type']
path = input['path']
c_name = input['c_name'].replace(" ", "")

f = urllib.request.urlopen(path)
mime_type = f.info().get_content_type()
f_ext = f.info().get_content_type().split("/")[1]

#https://developers.marketo.com/rest-api/assets/files/#create_and_update
url = "https://###-xxx-###.mktorest.com/rest/asset/v1/files.json"

content_type = {"Case Study": ["CaseStudy", "169"] , "eBook":["eBook","1569"], "Fact Sheet":["FactSheet","2076"], "Infographic":["Infographic","2070"], "Guide":["Guide","2076"], "Whitepaper":["Whitepaper","2067"]}

f_name = 'Content_'+content_type[c_type][0]+'_'+c_name + '.' + f_ext

payload = {
'folder': '{"id":'+content_type[c_type][1]+',"type":"Folder"}'
}

headers = {
  'Authorization': 'Bearer ' + input['token']
}

files = {'file': (f_name, f, mime_type)}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))
f_url = re.search('"url":"(.*)","folder',response.text).group(1)

return {'file_url': f_url}
