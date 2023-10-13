
#input variables to Zapier Step 9: Get New Program ID
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'name' : 'Campaign Name', #from Step 1: New UTM Request Form Submission
  'sub-channel':'Sub-Channel', #from Step 3: Update Next Row In UTM Builder Sheet
  'channel':'Channel' #from Step 3: Update Next Row In UTM Builder Sheet
  }

import re
import datetime

now = datetime.datetime.now()
year = str(now.year) 
month = str(now.month)

if len(month)==1:
        month =  "0" + month

sub-channel = input['sub-channel']

mapping = {'Advertising':'Digital Advertising','Paid_Search':'Paid Search',}
channel = mapping[input['channel']]

prog_name = year + month + " - " + channel + " - " + sub-channel + " - " + re.search('\s([\w*\s]+)', input['name']).group(1)

print(prog_name)

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/folder/byName.json?name="+prog_name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)
pid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
url = re.search('"url":"(.*?)",', response.text).group(1)
return {'pid': pid,'name':prog_name, 'url': url}
