# input variables to Zapier Code Transfer Step 11: Get Temporary Links
input = {
    'token': 'Token',  # from Step 4: Get Marketo Access Token
    'parent id': 'fid',  # from Step 5: Get Parent ID or Create Parent Folder
}

import re
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import json
import ast

url = "https://api.dropboxapi.com/2/files/get_temporary_link"
headers = {
    'Authorization': 'Bearer xxx',
    'Content-Type': 'application/json'
}

m = ast.literal_eval(input['dict'])
mapping = {k: v for k, v in m.items() if k is not ''}

links = []

for key, value in mapping.items():
    if re.match('https://www.dropbox.com', value):
        path = urlparse(value).path
        path = re.search("(/Telnyx.*$)", path).group(0).lower()
        path = unquote(path)

        payload = {"path": path}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).text
        print(response)
        dbx = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response).group(0)

        mapping[key] = [value, dbx]

return {'dict': str(mapping)}
