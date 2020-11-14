#input variables to Zapier Step 5: Get Rebrandly Link
input={
  'slash_tag': 'Rebrandly Slash Tag' #from Step 1: Get Submission from Google Form
  'dest': 'File URL' #from Step 4: Upload File to Marketo
  }

import requests
import json

if '.png' in input['dest']:
    dest = input['dest']
else:
    dest = 'http://go.telnyx.com/redirector.html#' + input['dest']

#https://developers.rebrandly.com/docs
linkRequest = {
  "destination": dest
  , "domain": { "fullName": "tlyx.co" }
 , "slashtag": input['slash_tag']
}

requestHeaders = {
  "Content-type": "application/json",
  "apikey": "xxxxx"
}

r = requests.post("https://api.rebrandly.com/v1/links",
    data = json.dumps(linkRequest),
    headers=requestHeaders)

if (r.status_code == requests.codes.ok):
    link = r.json()
    print("Long URL was %s, short URL is %s" % (link["destination"], link["shortUrl"]))
    return {'rebrandly_url': link["shortUrl"]}
