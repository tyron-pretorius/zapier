#input variables to Developer Newsletter Creation Step 10: Get Temporary Links
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import re
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import json

url = "https://api.dropboxapi.com/2/files/get_temporary_link"
headers = {
  'Authorization': 'Bearer xxx',
  'Content-Type': 'application/json'
}

links = input['links'].split("*")
paths = ['']*len(links)
response = [None]*len(links)
dbx_links = ['']*len(links)

for i in range(0,len(paths)):
    paths[i]  = urlparse(links[i]).path
    paths[i] = re.search("(/Telnyx.*$)",paths[i]).group(0).lower()
    paths[i] = unquote(paths[i])

    print(paths[i])
    payload = {"path": paths[i]}
    response[i] = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    print(response[i].text)

    dbx_links[i] = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response[i].text).group(0)

return {'dbx_links': dbx_links}
