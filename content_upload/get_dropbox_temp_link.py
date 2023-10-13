#input variables to Zapier Step 2: Get Dropbox Temporary Link
input={
  'link': 'Dropbox path for content' #from Step 1: Get Submission from Google Form
  }

import re
from urllib.parse import urlparse
from urllib.parse import unquote
import requests
import json

#https://www.dropbox.com/developers/documentation/http/documentation#files-get_temporary_link

path  = urlparse(input["link"]).path
path = re.search("(/Telnyx.*$)",path).group(0).lower()
path = unquote(path)

print(path)

url = "https://api.dropboxapi.com/2/files/get_temporary_link"
payload = {"path": path}

headers = {
  'Authorization': 'Bearer xxxx',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

print(response)

link = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.text).group(0)

return {'content_link': link}
