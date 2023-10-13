#input variables to Zapier Step 9: Upload Images to Marketo
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'paths': 'Dbx Links' #from Step 8: Get Temporary Dropbox Links
  'dbx': 'Dropbox Values' #from Step 1: New Spreadsheet Row
}

import requests
import urllib
import json
import re

payload = {
'folder': '{"id":367,"type":"Folder"}' #Email Files folder
}

headers = {
  'Authorization': 'Bearer ' + input['token']
}

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/files.json"

links = input['dbx'].split("*")
dbx_links = input['paths'].split(",")

paths = ['']*len(links)
names = ['']*len(links)

response = [None]*len(links)
mkto_url = [None]*len(links)

for i in range(0,len(paths)):
    paths[i]  = urllib.parse.urlparse(links[i]).path
    paths[i] = re.search("(/Telnyx.*$)",paths[i]).group(0).lower()
    paths[i] = urllib.parse.unquote(paths[i])
    names[i] = paths[i].split("/")[-1]
    names[i] = re.sub(r'[\s-]','_',names[i])

    f = urllib.request.urlopen(dbx_links[i])
    mime_type = f.info().get_content_type()

    if i==1:
        f_name = 'Asset_Email_Banner_'+names[i]
    else:
        f_name = 'Asset_Email_Thumbnail_'+names[i]

    files = {'file': (f_name, f, mime_type)}

    response[i] = requests.request("POST", url, headers=headers, data = payload, files = files)
    
    print(response[i].text)
    mkto_url[i] = re.search('"url":"(.*)","folder',response[i].text).group(1)

return {'mkto_urls': mkto_url}
